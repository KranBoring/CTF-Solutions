<?php
require_once __DIR__ . '/config.php';
require_once __DIR__ . '/json.php';
require_once __DIR__ . '/calendar.php';
require_once __DIR__ . '/crypto.php';

const SEAT_RE = '/^[A-F](0[1-9]|1[0-2])$/';

function nonce_key(): string {
    static $key = null;
    return $key ??= hash('sha256', 'hacker-cinema-nonce-key|' . nonce_seed(), true);
}

function derive_nonce(array $ticket, int $screeningTs): GMP {
    $domain = [
        'movie' => $ticket['movie'],
        'screen' => $ticket['screen'],
        'seat' => $ticket['seat'],
        'date' => kiosk_partition_date($screeningTs),
        'winner' => $ticket['winner'],
    ];
    $material = hash_hmac('sha256', 'ticket-v1|' . canonical_json($domain), nonce_key(), true);
    return gmp_add(gmp_mod(gmp_from_bytes($material), gmp_sub(N(), 1)), 1);
}

function miracle_winner(string $seat, int $screeningTs): bool {
    return hash('sha256', 'neon-jackpot|' . $seat . '|' . $screeningTs) === str_repeat('0', 64);
}

function make_ticket(string $seat, int $screeningTs): array {
    if (!preg_match(SEAT_RE, $seat)) {
        throw new InvalidArgumentException('invalid seat');
    }
    $ticket = [
        'date' => ticket_date_from_timestamp($screeningTs),
        'movie' => MOVIE,
        'screen' => SCREEN,
        'seat' => $seat,
        'winner' => miracle_winner($seat, $screeningTs),
    ];
    $message = canonical_json($ticket);
    [$r, $s] = ecdsa_sign($message, derive_nonce($ticket, $screeningTs));
    $envelope = [
        'ticket' => $ticket,
        'signature' => [
            'alg' => 'ECDSA-secp256k1-SHA256',
            'r' => hex64($r),
            's' => hex64($s),
        ],
    ];
    return [$envelope, canonical_json($envelope)];
}

function verify_envelope(string $payload): array {
    $env = json_decode($payload, true, flags: JSON_THROW_ON_ERROR);
    if (!is_array($env) || !isset($env['ticket'], $env['signature'])) {
        throw new InvalidArgumentException('ticket envelope is incomplete');
    }
    $ticket = $env['ticket'];
    $sig = $env['signature'];
    if (!is_array($ticket) || !is_array($sig)) {
        throw new InvalidArgumentException('ticket envelope is malformed');
    }
    if (($sig['alg'] ?? '') !== 'ECDSA-secp256k1-SHA256') {
        throw new InvalidArgumentException('unsupported ticket type');
    }
    foreach (['date', 'movie', 'screen', 'seat', 'winner'] as $field) {
        if (!array_key_exists($field, $ticket)) {
            throw new InvalidArgumentException('ticket is missing fields');
        }
    }
    if (!preg_match(SEAT_RE, (string)$ticket['seat'])) {
        throw new InvalidArgumentException('invalid seat');
    }
    if (!is_bool($ticket['winner'])) {
        throw new InvalidArgumentException('invalid prize marker');
    }
    $r = gmp_from_hex((string)($sig['r'] ?? ''));
    $s = gmp_from_hex((string)($sig['s'] ?? ''));
    $ok = ecdsa_verify(canonical_json($ticket), $r, $s);
    return [$ticket, $ok];
}
