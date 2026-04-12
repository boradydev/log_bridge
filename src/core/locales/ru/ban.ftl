BAN =
    🚫 Забанен { $email } на { $duration ->
        [one] { $duration } минуту
        [few] { $duration } минуты
       *[other] { $duration } минут
    }. IP клиента: { $client_ip }

UNBAN = ✅ Разбанен { $email }. IP клиента: { $client_ip }
