
//override defaults
alertify.defaults.transition = "slide";
alertify.defaults.theme.ok = "btn btn-primary";
alertify.defaults.theme.cancel = "btn btn-danger";
alertify.defaults.theme.input = "form-control";

$("#gnrateqrcode").on('click', function (e) {
  var userInput = $("#prodcode").val();
  console.log(userInput);
  if(userInput != ""){
    userInput = userInput;
  }else{
    alertify.error("Pleas Input Product Code");
    return;
  }
  $(".gntdqr").show();
  $("#gnimg").html("");
  var qrcode = new QRCode("gnimg", {
    text: userInput,
    width: 128,
    height: 128,
    colorDark : "#000000",
    colorLight : "#ffffff",
    correctLevel : QRCode.CorrectLevel.H
  });


  $("form").on("submit", function (e) {  e.preventDefault(); });



});