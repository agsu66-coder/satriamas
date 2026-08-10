const cache = new Map();

module.exports = {

    save(messageId, aduanId) {

        cache.set(messageId, aduanId);

    },

    get(messageId) {

        return cache.get(messageId);

    }

};