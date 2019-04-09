function ShowFlashMessage(message){
  var template = "<div class='container container-alert-flash'>"+"<div class='col-sm-4 offset-sm-7'>"+"<div class='alert alert-success' role='alert'>"+message+"</div></div></div>"

  $("body").append(template);
  $(".container-alert-flash").fadeIn();
  setTimeout(function(){
    console.log("this function is working.")
    $(".container-alert-flash").fadeOut();
  }, 1800);
}
