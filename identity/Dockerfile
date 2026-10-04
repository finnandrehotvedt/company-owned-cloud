FROM quay.io/keycloak/keycloak:26.3.3@sha256:6a7217a100bd3e5de4063a27a538ef999a3c5a88c4b4ec0ffc0a642aee7b2597

USER 0
COPY identity/entrypoint.sh /opt/lab/entrypoint.sh
COPY identity/realm.json /opt/lab/realm.json
RUN chmod 0755 /opt/lab/entrypoint.sh && chmod 0644 /opt/lab/realm.json
USER 1000

ENTRYPOINT ["/opt/lab/entrypoint.sh"]
