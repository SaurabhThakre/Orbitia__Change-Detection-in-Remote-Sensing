

$('#sendSegmentation').submit(async function(){
    console.log("vvvvv")
    event.preventDefault();
  
    var form = $('#sendSegmentation')[0];
  
    var dataImg = new FormData(form);
  
    dataImg.append("CustomField", "This is testing");
    
    console.log(dataImg);

    if(document.getElementById('loadingmessage2').style.display == 'none'){
      document.getElementById("loadingmessage2").style.display = "block";
    }
  
    await $.ajax({
      url: "/segmentation",
      enctype: 'multipart/form-data',
      type: 'POST',
      processData: false,
      contentType: false,
      cache: false,
      data : dataImg,
  
      success: function(res){
        console.log(res);

        // image display------------------------------------------------------------
        var input1 = res.input;
        var input2 = res.output;

        var e = $(`
        <div class="row">
          <div class="column" style="width: 50%;">
            <h5> Natural Image</h5>
            <img src="${input1}" alt="img1" style="width:80%">
          </div>
          <br/>
          <div class="column" style="width: 50%">
            <h5>Features Extracted Image</h5>
            <img src="${input2}" alt="img2" style="width:80%">
          </div>
        </div>
        
        `);        
        $('#displayOutput').append(e);
        // image display ends ------------------------------------------------------
        
      },
  
      error: function(request, status, error) {
        console.log(status);
      }
  
    });

    document.getElementById("loadingmessage2").style.display = "none";

  });
  
  
  
  