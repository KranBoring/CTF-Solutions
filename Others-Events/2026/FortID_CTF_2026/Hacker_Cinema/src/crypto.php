<?php
require_once __DIR__ . '/config.php';

if (!extension_loaded('gmp')) {
    throw new RuntimeException('Hacker Cinema ticket signer requires the PHP GMP extension.');
}

function P(): GMP { static $v = null; return $v ??= gmp_init('0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F'); }
function N(): GMP { static $v = null; return $v ??= gmp_init('0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141'); }
function Gx(): GMP { static $v = null; return $v ??= gmp_init('0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798'); }
function Gy(): GMP { static $v = null; return $v ??= gmp_init('0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8'); }
function G(): array { return [Gx(), Gy()]; }

function mod_g(GMP|int|string $x, GMP $m): GMP {
    $r = gmp_mod($x, $m);
    return gmp_cmp($r, 0) < 0 ? gmp_add($r, $m) : $r;
}

function inv_mod(GMP|int|string $x, GMP $m): GMP {
    $inv = gmp_invert(mod_g($x, $m), $m);
    if ($inv === false) {
        throw new RuntimeException('non-invertible scalar');
    }
    return $inv;
}

function point_add(?array $p, ?array $q): ?array {
    if ($p === null) return $q;
    if ($q === null) return $p;
    [$x1, $y1] = $p;
    [$x2, $y2] = $q;
    $prime = P();

    if (gmp_cmp($x1, $x2) === 0 && gmp_cmp(mod_g(gmp_add($y1, $y2), $prime), 0) === 0) {
        return null;
    }

    if (gmp_cmp($x1, $x2) === 0 && gmp_cmp($y1, $y2) === 0) {
        $lambda = mod_g(gmp_mul(gmp_mul(3, gmp_mul($x1, $x1)), inv_mod(gmp_mul(2, $y1), $prime)), $prime);
    } else {
        $lambda = mod_g(gmp_mul(gmp_sub($y2, $y1), inv_mod(gmp_sub($x2, $x1), $prime)), $prime);
    }

    $x3 = mod_g(gmp_sub(gmp_sub(gmp_mul($lambda, $lambda), $x1), $x2), $prime);
    $y3 = mod_g(gmp_sub(gmp_mul($lambda, gmp_sub($x1, $x3)), $y1), $prime);
    return [$x3, $y3];
}

function scalar_mul(GMP|int|string $k, ?array $point = null): ?array {
    $k = mod_g($k, N());
    $result = null;
    $addend = $point ?? G();
    while (gmp_cmp($k, 0) > 0) {
        if (gmp_testbit($k, 0)) {
            $result = point_add($result, $addend);
        }
        $addend = point_add($addend, $addend);
        $k = gmp_div_q($k, 2);
    }
    return $result;
}

function gmp_from_bytes(string $bytes): GMP {
    $value = gmp_import($bytes, 1, GMP_MSW_FIRST | GMP_BIG_ENDIAN);
    return $value === false ? gmp_init(0) : $value;
}

function sha256_int(string $data): GMP {
    return mod_g(gmp_from_bytes(hash('sha256', $data, true)), N());
}

function int_from_seed(string $label, string $seed): GMP {
    $value = gmp_from_bytes(hash('sha256', $label . '|' . $seed, true));
    return gmp_add(gmp_mod($value, gmp_sub(N(), 1)), 1);
}

function private_key(): GMP {
    static $d = null;
    return $d ??= int_from_seed('hacker-cinema-signing-key', signing_seed());
}

function public_key(): array {
    static $q = null;
    return $q ??= scalar_mul(private_key());
}

function hex64(GMP $x): string {
    return str_pad(gmp_strval($x, 16), 64, '0', STR_PAD_LEFT);
}

function gmp_from_hex(string $hex): GMP {
    if (!preg_match('/^[0-9a-fA-F]+$/', $hex)) {
        throw new InvalidArgumentException('invalid scalar encoding');
    }
    return gmp_init('0x' . $hex);
}

function ecdsa_sign(string $message, GMP $k): array {
    $n = N();
    $z = sha256_int($message);
    $k = mod_g($k, $n);
    if (gmp_cmp($k, 0) === 0) {
        throw new RuntimeException('bad ticket nonce');
    }
    $rPoint = scalar_mul($k);
    if ($rPoint === null) {
        throw new RuntimeException('bad ticket nonce');
    }
    $r = mod_g($rPoint[0], $n);
    if (gmp_cmp($r, 0) === 0) {
        throw new RuntimeException('bad ticket nonce');
    }
    $s = mod_g(gmp_mul(inv_mod($k, $n), gmp_add($z, gmp_mul($r, private_key()))), $n);
    if (gmp_cmp($s, 0) === 0) {
        throw new RuntimeException('bad ticket nonce');
    }
    return [$r, $s];
}

function ecdsa_verify(string $message, GMP $r, GMP $s): bool {
    $n = N();
    if (gmp_cmp($r, 1) < 0 || gmp_cmp($r, $n) >= 0 || gmp_cmp($s, 1) < 0 || gmp_cmp($s, $n) >= 0) {
        return false;
    }
    $z = sha256_int($message);
    try {
        $w = inv_mod($s, $n);
    } catch (Throwable) {
        return false;
    }
    $u1 = mod_g(gmp_mul($z, $w), $n);
    $u2 = mod_g(gmp_mul($r, $w), $n);
    $p = point_add(scalar_mul($u1), scalar_mul($u2, public_key()));
    if ($p === null) {
        return false;
    }
    return gmp_cmp(mod_g($p[0], $n), $r) === 0;
}
