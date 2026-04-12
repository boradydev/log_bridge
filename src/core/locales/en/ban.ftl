BAN =
    🚫 Banned { $email } for { $duration ->
        [one] { $duration } minute
       *[other] { $duration } minutes
    }. Client IP: { $client_ip }

UNBAN = ✅ Unbanned { $email }. Client IP: { $client_ip }