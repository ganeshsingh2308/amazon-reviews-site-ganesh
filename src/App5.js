fetch('http://127.0.0.1:5000/test6')
.then(function (response) {
    return response.json();
}).then(function (text) {
    console.log('GET response:');
    console.log(text);
    document.getElementById('test6').innerHTML = '';
    for (var i = 0; i < text.length ; i++) {
        document.getElementById('test6').innerHTML += '<tr> <td><button>' + text[i]['keyword'] + '</button></td>' + '<td>' + text[i]['mentions'] + '</td>' + '<td>' + text[i]['positive'] + '</td>' + '<td>' + text[i]['negative'] + '</td>' + '<td>' + text[i]['averagerating'] + '</td></tr>' ; 
      };
    
});


