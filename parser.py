use codex_network_proxy::{NetworkProxy, NetworkDecision, NetworkPolicyRequest};

let proxy = NetworkProxy::builder()
    .http_addr("127.0.0.1:8080".parse()?)
    .policy_decider(|request: NetworkPolicyRequest| async move {
        // Example: auto-allow when exec policy already approved a command prefix.
        if let Some(command) = request.command.as_deref() {
            if command.starts_with("curl ") {
                return NetworkDecision::Allow;
            }
        }
        NetworkDecision::Deny {
            reason: "policy_denied".to_string(),
        }
    })
    .build()
    .await?;

let handle = proxy.run().await?;
handle.shutdown().await?;
