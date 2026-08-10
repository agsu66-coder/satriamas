/**
 * ==========================================================
 * TERATAI AI
 * Configuration
 * ==========================================================
 */

const BACKEND_URL = "http://127.0.0.1:5000";

module.exports = {

    // Backend
    BACKEND_URL,

    // API Endpoint
    AI_ENDPOINT: `${BACKEND_URL}/ask`,
    TEMPLATE_ENDPOINT: `${BACKEND_URL}/template`,
    RELOAD_ENDPOINT: `${BACKEND_URL}/reload`,
    HEALTH_ENDPOINT: `${BACKEND_URL}/health`

};