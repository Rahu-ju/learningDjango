// For flash message
function ShowFlashMessage(message){
  var template = "<div class='container container-alert-flash'>"+"<div class='col-sm-4 offset-sm-7'>"+"<div class='alert alert-success' role='alert'>"+message+"</div></div></div>"

  $("body").append(template);
  $(".container-alert-flash").fadeIn();
  setTimeout(function(){
    console.log("this function is working.")
    $(".container-alert-flash").fadeOut();
  }, 1800);
}

// Show cart item in navbar using ajax
function updateCartItemCount(){
  // Django template tag is not recognise inside js
  // ie. we get the data-url attribute that is actually {% url "item_count" %} in the navbar template
  var url = $("#cart_item_badge").attr("data-url");
  $.ajax({
    type: "GET",
    url: url,
    success:function(data){
      console.log(data.cart_item);
      $("#cart_item_badge").text(data.cart_item)
    },
    error:function(response, error){
      console.log(response);
      console.log(error);
    },
  })
}

$(document).ready(function(){
  updateCartItemCount();
})
