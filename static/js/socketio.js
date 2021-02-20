document.addEventListener('DOMContentLoaded', () => {
    var socket = io.connect('http://'+document.domain+':'+location.port);

    let room = document.getElementById('curr_room').innerText;
    joinRoom(room);
    
    var room_id = document.getElementById('curr_room_id').innerText;
    console.log(room_id);
    
    socket.on('message', data => {
        
        const p = document.createElement('p');
        const span_username = document.createElement('span');
        const span_timestamp = document.createElement('span');
        const br = document.createElement('br');

        if (data.uname) {
            span_username.innerHTML = data.uname;
            span_timestamp.innerHTML = data.time_stamp;

            p.innerHTML = span_username.outerHTML + br.outerHTML + data.msg + br.outerHTML
                          + span_timestamp.outerHTML;
            document.querySelector('#display_message_section').append(p);
            
        } else {
            printSysMsg(data.msg);
        }
        
    });

    document.querySelector('#send_message').onclick = () => {
        console.log(room_id )
        socket.send({'msg': document.querySelector('#user_message').value,
                     'uname': curr_uname, 'room': room, 'room_id': room_id });

        document.getElementById('user_message').value="";
    }

    document.querySelectorAll('#select-room').forEach(p => {
        p.onclick = () => {
            let newRoom = p.innerHTML;

            if (newRoom == room) {
                msg = `You are already in ${room} room.`
                printSysMsg(msg);
            } else {
                leaveRoom(room);
                joinRoom(newRoom);
                room = newRoom;
            }
        }
    });

    function leaveRoom(room) {
        socket.emit('leave', {'uname': curr_uname, 'room':room});
    }

    function joinRoom(room) {
        socket.emit('join', {'uname': curr_uname, 'room':room});

        document.querySelector('#display_message_section').innerHTML = '';

        document.querySelector('#user_message').focus();

        document.getElementById('curr_room').innerText = room;
    }

    function printSysMsg(msg) {
        const p = document.createElement('p');
        p.innerHTML = msg
        document.querySelector('#display_message_section').append(p);
    }

})