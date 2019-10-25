console.log("Linked")

var submit = document.getElementById('button')
var select = document.getElementById('select')

submit.addEventListener("click",function(){
  console.log("Clicked")
  var xhttp = new XMLHttpRequest()
  xhttp.onreadystatechange = function(){
    if(this.readyState===4 && this.status===200){
      var val=JSON.parse(this.responseText);
      
      document.getElementById('fig1').innerHTML=val.fig1;
      document.getElementById('fig2').innerHTML=val.fig2;
      document.getElementById('fig1_a').innerHTML=val.fig1_a;
      print(val.fig1)
      document.getElementById('fig2_a').innerHTML=val.fig2_a;
    }
  }
  xhttp.open('POST','/kmeans/perform/',true)
  xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  xhttp.send("type="+select.options[select.selectedIndex].value)
})