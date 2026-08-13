// POPCORN 0.02v
// frontend/js/account.js

const API_URL = "http://127.0.0.1:8000";
const ACCOUNT_STORAGE_KEY = "popcorn_account";


async function createServerAccount() {
    try {
        const response = await fetch(`${API_URL}/accounts`, {
            method: "POST"
        });

        if (!response.ok) {
            throw new Error(`Server returned ${response.status}`);
        }

        const data = await response.json();

        if (!data.success || !data.account) {
            throw new Error("Invalid account response");
        }

        localStorage.setItem(
            ACCOUNT_STORAGE_KEY,
            JSON.stringify(data.account)
        );

        return data.account;

    } catch (error) {
        console.error(
            "❌ Failed to create POPCORN account:",
            error
        );

        return null;
    }
}


async function getServerAccount(accountId) {
    try {
        const response = await fetch(
            `${API_URL}/accounts/${encodeURIComponent(accountId)}`
        );

        if (!response.ok) {
            return null;
        }

        const data = await response.json();

        if (!data.success || !data.account) {
            return null;
        }

        return data.account;

    } catch (error) {
        console.error(
            "❌ Failed to get POPCORN account:",
            error
        );

        return null;
    }
}


async function getAccount() {
    const savedAccount =
        localStorage.getItem(ACCOUNT_STORAGE_KEY);

    // Account already exists in this browser
    if (savedAccount) {
        try {
            const account = JSON.parse(savedAccount);

            if (account.id) {
                const serverAccount =
                    await getServerAccount(account.id);

                if (serverAccount) {
                    localStorage.setItem(
                        ACCOUNT_STORAGE_KEY,
                        JSON.stringify(serverAccount)
                    );

                    return serverAccount;
                }
            }

        } catch (error) {
            console.error(
                "❌ Failed to read saved account:",
                error
            );
        }
    }

    // No account found, create a new one
    return await createServerAccount();
}


async function getAccountId() {
    const account = await getAccount();

    if (!account) {
        return null;
    }

    return account.id;
}


async function displayAccount() {
    const account = await getAccount();

    if (!account) {
        console.error(
            "❌ Could not load POPCORN account."
        );

        return;
    }

    const accountIdElement =
        document.getElementById("account-id");

    if (accountIdElement) {
        accountIdElement.textContent = account.id;
    }

    const createdAtElement =
        document.getElementById("account-created");

    if (createdAtElement && account.createdAt) {
        const date = new Date(account.createdAt);

        createdAtElement.textContent =
            date.toLocaleDateString();
    }

    console.log(
        "🍿 POPCORN Account ID:",
        account.id
    );
}


async function copyAccountId() {
    const accountId = await getAccountId();

    if (!accountId) {
        alert("Account ID is unavailable.");
        return;
    }

    try {
        await navigator.clipboard.writeText(accountId);

        alert("Account ID copied! 📋");

    } catch (error) {
        console.error(
            "❌ Failed to copy Account ID:",
            error
        );

        alert("Could not copy Account ID.");
    }
}


async function initializeAccount() {
    await displayAccount();
}


document.addEventListener(
    "DOMContentLoaded",
    initializeAccount
);