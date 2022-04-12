$('#sendImages').submit( async function(){
  console.log("vvvvv")
  event.preventDefault();

  var form = $('#sendImages')[0];

  var dataImg = new FormData(form);

  dataImg.append("CustomField", "This is some extra data, testing");
  
  console.log( document.getElementById("loadingmessage").style.display);
  if(document.getElementById('loadingmessage').style.display == 'none'){
    document.getElementById("loadingmessage").style.display = "block";
  }
  
  await $.ajax({
    url: "/pcaanalysis",
    enctype: 'multipart/form-data',
    type: 'POST',
    processData: false,
    contentType: false,
    cache: false,
    data : dataImg,

    success: function(res){
      console.log(res);
      if(res.status == 'Success'){
        console.log(res.img1)
        var input1 = "static/upload_pca/" + res.img1;
        var input2 = "static/upload_pca/" + res.img2;
        var result = "static/upload_pca/" + res.imagePath;
        console.log(result);

        
        var e = $(`
        <div class="row">
          <div class="column">
            <img src="${input1}" alt="img1" style="width:55%">
            <p>Image A</p>
          </div>
          <div class="column">
            <img src="${input2}" alt="img2" style="width:55%">
            <p>Image B</p>
          </div>
        </div>
        <div class="row">
          <div class="column">
            <h4>After PCA result is: </h4>
            <img src="${result}" alt="result" style="width:55%">
          </div>
        </div>
        <br/>
        <br/>
      `);        
        $('#displayImg').append(e);    
        // e.attr('id', 'myid');
      
      }
    },

    error: function(request, status, error) {
      console.log(status)
    }

  });
   document.getElementById("loadingmessage").style.display = "none";
});



