<?php
require_once __DIR__ . '/config.php';

function store_dir(): string {
    $dir = sys_get_temp_dir() . DIRECTORY_SEPARATOR . 'hacker_cinema_tickets';
    if (!is_dir($dir)) {
        @mkdir($dir, 0700, true);
    }
    return $dir;
}

function put_ticket(string $payload): string {
    $id = rtrim(strtr(base64_encode(random_bytes(16)), '+/', '-_'), '=');
    file_put_contents(store_dir() . DIRECTORY_SEPARATOR . $id . '.json', $payload, LOCK_EX);
    $files = glob(store_dir() . DIRECTORY_SEPARATOR . '*.json') ?: [];
    if (count($files) > MAX_STORED_TICKETS) {
        usort($files, fn($a, $b) => filemtime($a) <=> filemtime($b));
        foreach (array_slice($files, 0, count($files) - MAX_STORED_TICKETS) as $old) {
            @unlink($old);
        }
    }
    return $id;
}

function get_ticket(string $id): ?string {
    if (!preg_match('/^[A-Za-z0-9_-]{10,80}$/', $id)) {
        return null;
    }
    $path = store_dir() . DIRECTORY_SEPARATOR . $id . '.json';
    if (!is_file($path)) {
        return null;
    }
    return file_get_contents($path);
}
