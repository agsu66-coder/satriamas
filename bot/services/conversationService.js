const conversations = new Map();

function set(user, data) {

    conversations.set(user, data);

}

function get(user) {

    return conversations.get(user);

}

function clear(user) {

    conversations.delete(user);

}

module.exports = {

    set,

    get,

    clear

};