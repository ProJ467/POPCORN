// POPCORN 0.02v
// frontend/js/main.js

const API_URL = "http://127.0.0.1:8000";


async function checkServer() {
    try {
        const response = await fetch(`${API_URL}/health`);

        if (!response.ok) {
            throw new Error(`Server returned ${response.status}`);
        }

        const data = await response.json();

        console.log("🍿 POPCORN server:", data.status);

        return true;

    } catch (error) {
        console.error("❌ POPCORN server is unavailable:", error);

        return false;
    }
}


document.addEventListener("DOMContentLoaded", () => {
    checkServer();
});