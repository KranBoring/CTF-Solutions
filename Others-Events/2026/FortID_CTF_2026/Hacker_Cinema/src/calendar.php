<?php
require_once __DIR__ . '/config.php';

function ticket_date_from_timestamp(int $ts): string {
    $dt = DateTimeImmutable::createFromFormat('U', (string)$ts);
    if ($dt === false) {
        throw new RuntimeException('ticket calendar rejected the screening');
    }
    return $dt->setTimezone(new DateTimeZone('UTC'))->format('Y-m-d');
}

function kiosk_partition_date(int $ts): string {
    $dt = new DateTimeImmutable('@' . (string)$ts);
    return $dt->setTimezone(new DateTimeZone('UTC'))->format('Y-m-d');
}

function timestamp_for_show_date(string $date): int {
    if (!preg_match('/^\d{4}-\d{2}-\d{2}$/', $date)) {
        throw new InvalidArgumentException('invalid screening date');
    }
    $dt = new DateTimeImmutable($date . sprintf(' %02d:00:00 UTC', SHOW_HOUR_UTC), new DateTimeZone('UTC'));
    return $dt->getTimestamp();
}

function future_dates(): array {
    $tomorrow = (new DateTimeImmutable('tomorrow', new DateTimeZone('UTC')))->format('Y-m-d');
    return [$tomorrow, $tomorrow, timestamp_for_show_date($tomorrow)];
}
