<?php
const MOVIE = 'Hackers';
const MOVIE_YEAR = 1995;
const SCREEN = 'mainframe-1';
const SHOW_HOUR_UTC = 20;
const MAX_STORED_TICKETS = 256;
const MIN_SCREENING_TS = -70000000000;
const MAX_SCREENING_TS = 4102444800;

function env_or_file_secret(string $envName, string $fileName): string {
    $value = getenv($envName);
    if ($value !== false && $value !== '') {
        return $value;
    }
    $path = sys_get_temp_dir() . DIRECTORY_SEPARATOR . $fileName;
    if (is_file($path)) {
        $stored = trim((string)file_get_contents($path));
        if ($stored !== '') {
            return $stored;
        }
    }
    $secret = bin2hex(random_bytes(32));
    @file_put_contents($path, $secret, LOCK_EX);
    return $secret;
}

function signing_seed(): string {
    static $seed = null;
    if ($seed === null) {
        $seed = env_or_file_secret('HCINEMA_SIGNING_SEED', 'hacker_cinema_signing_seed');
    }
    return $seed;
}

function nonce_seed(): string {
    static $seed = null;
    if ($seed === null) {
        $seed = env_or_file_secret('HCINEMA_NONCE_SEED', 'hacker_cinema_nonce_seed');
    }
    return $seed;
}

function flag_path(): string {
    $value = getenv('FLAG_PATH');
    return ($value !== false && $value !== '') ? $value : dirname(__DIR__) . '/flag.txt';
}
