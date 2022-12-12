fetch('http://127.0.0.1:5000/test')
.then(function (response) {
    return response.json();
}).then(function (text) {
    console.log('GET response:');
    console.log(text);
    document.getElementById('test').innerHTML = "<p>Total reviews:</p>" + text[0]; 
    document.getElementById('test1').innerHTML = "<p>Average Rating:</p>" + text[3]; 
    document.getElementById('test2').innerHTML = "<p>Negative Ratings:</p>" + text[2]; 
    document.getElementById('test3').innerHTML = "<p>Positive Ratings:</p>" + text[1];
    
    
    
});


