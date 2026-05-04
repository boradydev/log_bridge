success =
    ✅ { $hostname }: connection ssh
    user: { $user }
    ip: { $client_ip }
disconnect =
    ℹ️ { $hostname }: disconnection ssh
    user: { $user }
    ip: { $client_ip }
invalid_user =
    ⚠️ { $hostname }: Invalid user ssh
    ip: { $client_ip }
auth_failure =
    🚫 { $hostname }: Auth failure ssh
    user: { $user }
    ip: { $client_ip }