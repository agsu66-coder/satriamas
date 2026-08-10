const states = new Map();

function setState(user, data) {

    states.set(user, data);

}

function getState(user) {

    return states.get(user);

}

function clearState(user) {

    states.delete(user);

}

module.exports = {

    setState,

    getState,

    clearState

};