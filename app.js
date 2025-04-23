// noinspection JSJQueryEfficiency,JSUnresolvedReference,DuplicatedCode

function getKCHost() {
    let baseURL = "http://localhost/idp-auth";
    setTimeout(function () {
        kcAuth(baseURL);
    }, 2000);
}

function kcAuth(kcBaseURL) {
    const authURL = `${kcBaseURL}/idp-auth`;
    const keycloak = new Keycloak({
        "auth-server-url": authURL,
        url: kcBaseURL,
        realm: 'my-idp',
        clientId: 'my-idp-client',
        "enable-cors": true,
        "public-client": false,
    });

    keycloak.init({
        onLoad: 'check-sso',
        checkLoginIframe: false,
        promiseType: 'native',
        flow: 'implicit'
    }).then(isAuthenticated => {
        if (isAuthenticated) {
            console.log("Authenticated.");
            console.log(keycloak);
            window.keycloak = keycloak;
            // $('#token').html(keycloak.token);
            const payload = parseJWT(keycloak.token);
            $('#token').html(JSON.stringify(payload, null, 2)); // The '2' specifies a 2-space indentation
            $('.editor').show();
            $('.loader').hide();
        } else {
            window.location.href = 'http://localhost/idp-auth/realms/my-idp/protocol/saml/clients/sso?RelayState=hello';
        }
        // this.setState({keycloak: keycloak, authenticated: authenticated});
    }).catch(error => {
        console.error("Keycloak initialization error:", error);
    });
}

$(document).ready(function () {
    $("#sp-btn").on("click", function () {
        // window.location.href = `http://localhost/idp-auth/realms/my-idp/protocol/saml/clients/sso?RelayState=world`;
        window.location.href = 'http://localhost/sp'
    });
});

$(document).ready(function () {
    $("#btn-logout").on("click", function () {
        window.location.href = "http://localhost/idp-auth/realms/my-idp/protocol/openid-connect/logout";
    });
})


function parseJWT(token) {
    if (!token) {
        throw new Error("Token is required");
    }
    const parts = token.split('.');
    if (parts.length !== 3) {
        throw new Error("Invalid JWT format");
    }
    const payload = parts[1];
    // Decode the payload from Base64Url
    const decodedPayload = JSON.parse(atob(payload.replace(/-/g, '+').replace(/_/g, '/')));
    return decodedPayload;
}