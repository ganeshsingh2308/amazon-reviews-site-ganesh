fetch('http://127.0.0.1:5000/test3')
.then(function (response) {
    return response.json();
}).then(function (text) {
    console.log('GET response:');
    console.log(text);
    document.getElementById('test4').innerHTML = '';
    for (var i = 0; i < text.length ; i++) {
        document.getElementById('test4').innerHTML += '<div id="inlineCheckbox1"><input class="form-check-input" type="checkbox" id="inlineCheckbox1" value="' + text[i] + '" name="productdata">' +'<label class="form-check-label" for="inlineCheckbox1">' + text[i]+ '</label></div>'; 
      };
    
});


