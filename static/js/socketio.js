document.addEventListener('DOMContentLoaded', () => {
    var socket = io.connect('//'+document.domain+':'+location.port);

    let room = document.getElementById('curr_room').innerText;
    
    var room_id = document.getElementById('curr_room_id').innerText;
    console.log(room_id);
    joinRoom(room_id);

    var objDiv = document.getElementById("chat_scroll");
    objDiv.scrollTop = objDiv.scrollHeight;
    
    socket.on('message', data => {
        
        const div = document.createElement('div');
        div.className = "chat_container"
        const p_username = document.createElement('p');
        const p_timestamp = document.createElement('span');
        p_timestamp.className = "time-right"
        const hr = document.createElement('hr');
        const p_message = document.createElement('p');

        if (data.uname) {
            p_message.innerHTML = data.msg
            p_username.innerHTML = data.fname + " " + data.lname;
            p_timestamp.innerHTML = data.time_stamp;

            div.innerHTML = p_username.outerHTML + hr.outerHTML + p_message.outerHTML
                          + p_timestamp.outerHTML;
            document.querySelector('#display_message_section').append(div);
            
        } else {
            printSysMsg(data.msg);
        }
        objDiv.scrollTop = objDiv.scrollHeight;
        
    });

    document.querySelector('#send_message').onclick = () => {
        if(!(document.getElementById('user_message').value==="")){
            console.log(room_id )
            socket.send({'msg': document.querySelector('#user_message').value,
                     'uname': curr_uname,'fname':curr_fname,'lname':curr_lname,
                     'room': room, 'room_id': room_id });

            document.getElementById('user_message').value="";
        }
    }    

    document.querySelectorAll('#select-room').forEach(p => {
        p.onclick = () => {
            let newRoom = p.getAttribute("room_id"); 
            console.log(newRoom)
            if (newRoom == room_id) {
                msg = `You are already in ${room} room.`
                printSysMsg(msg);
            } else {
                leaveRoom(room_id);
                joinRoom(newRoom);
                room_id = newRoom;
                room = p.innerHTML
                console.log(room)
            }
        }
    });

    function leaveRoom(room) {
        socket.emit('leave', {'uname': curr_uname, 'room':room_id, 'room_name': room});
    }

    function joinRoom(room) {
        socket.emit('join', {'uname': curr_uname, 'room':room_id, 'room_name': room});

        document.querySelector('#display_message_section').innerHTML = '';

        document.querySelector('#user_message').focus();

        document.getElementById('curr_room_id').innerText = room_id;
    }

    function printSysMsg(msg) {
        const p = document.createElement('p');
        p.innerHTML = msg
        document.querySelector('#display_message_section').append(p);
    }

})