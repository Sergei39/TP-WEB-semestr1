console.log('canal: ' + 'answer-quest-');
cent = new Centrifuge('ws://:8000/connection/websocket');
cent.setToken(token);
console.log('canal: ' + 'answer-quest-' + quest_id);
cent.subscribe('answer-quest-' + quest_id, function(msg) { console.log(msg) });
cent.connect()
