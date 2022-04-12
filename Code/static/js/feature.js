
console.log("eee")
$('#sendFeature').submit( async function(){
    console.log("vvvvv")
    event.preventDefault();
  
    var form = $('#sendFeature')[0];
  
    var dataImg = new FormData(form);
    

    dataImg.append("CustomField", "This is some extra data, testing");
    
    console.log(dataImg);

    if(document.getElementById('loadingmessage1').style.display == 'none'){
      document.getElementById("loadingmessage1").style.display = "block";
    }
  
    await $.ajax({
      url: "/featureExtraction",
      enctype: 'multipart/form-data',
      type: 'POST',
      processData: false,
      contentType: false,
      cache: false,
      data : dataImg,
  
      success: function(res){
        console.log(res);
        // -------------------------------------------------------------------
        // start

        var i1 = res.imagePath[0]
        // console.log(i1)
        var i2 = res.imagePath[1]
        var i3 = res.imagePath[2]
        var i4 = res.imagePath[3]
        var i5 = res.imagePath[4]
        var i6 = res.imagePath[5]
        var i7 = res.imagePath[6]

        var t1 = "abc"
        var t2 = "acv"
        var t3 = "acv"
        var t4 = "acv"
        var t5 = "acv"
        var t6 = "acv"
        var t7 = "acv"
        
        if(res.imagePath[0]=="null"){
            i1 = ""
            t1 = "This feature cannot be detected"
        }

        if(res.imagePath[1]=="null"){
            i2 = ""
            t2 = "This feature cannot be detected"
        }

        if(res.imagePath[2]=="null"){
            i3 = ""
            t3 = "This feature cannot be detected"
        }

        if(res.imagePath[3]=="null"){
            i4 = ""
            t4 = "This feature cannot be detected"
        }
        if(res.imagePath[4]=="null"){
            i5 = ""
            t5 = "This feature cannot be detected"
        }
        if(res.imagePath[5]=="null"){
            i6 = ""
            t6 = "This feature cannot be detected"
        }
        if(res.imagePath[6]=="null"){
            i7 = ""
            t7 = "This feature cannot be detected"
        }
       

        $('#allData').append($(`
        <div class="col-lg-4 col-md-6 portfolio-item filter-app">
          <div class="portfolio-wrap">
            <figure>
              <img src="${i1}" class="img-fluid" alt="" />
              <a
                href="${i1}"
                class="link-preview venobox"
                data-gall="portfolioGallery"
                title="Natural Color"
                target="_blank"
                ><i class="ion ion-eye"></i
              ></a>
            </figure>

            <div class="portfolio-info">
              <h4><a href="portfolio-details.html">Natural Color</a></h4>
              <p>${t1}</p>
            </div>
          </div>
        </div>

        <div class="col-lg-4 col-md-6 portfolio-item filter-web">
          <div class="portfolio-wrap">
            <figure>
              <img src="${i2}" class="img-fluid" alt="" />
              <a
                href="${i2}"
                class="link-preview venobox"
                data-gall="portfolioGallery"
                title="Geology"
                target="_blank"
                ><i class="ion ion-eye"></i
              ></a>
            </figure>

            <div class="portfolio-info">
              <h4><a href="portfolio-details.html">Geology</a></h4>
              <p>${t2}</p>
            </div>
          </div>
        </div>

        <div class="col-lg-4 col-md-6 portfolio-item filter-app">
          <div class="portfolio-wrap">
            <figure>
              <img src="${i3}" class="img-fluid" alt="" />
              <a
                href="${i3}"
                class="link-preview venobox"
                data-gall="portfolioGallery"
                title="NDVI"
                target="_blank"
                ><i class="ion ion-eye"></i
              ></a>
            </figure>

            <div class="portfolio-info">
              <h4><a href="portfolio-details.html">NDVI</a></h4>
              <p>${t3}</p>
            </div>
          </div>
        </div>

        <div class="col-lg-4 col-md-6 portfolio-item filter-card">
          <div class="portfolio-wrap">
            <figure>
              <img src="${i4}" class="img-fluid" alt="" />
              <a
                href="${i4}"
                class="link-preview venobox"
                data-gall="portfolioGallery"
                title="Bathymetric"
                target="_blank"
                ><i class="ion ion-eye"></i
              ></a>
            </figure>

            <div class="portfolio-info">
              <h4><a href="portfolio-details.html">Bathymetric</a></h4>
              <p>${t4}</p>
            </div>
          </div>
        </div>

        <div class="col-lg-4 col-md-6 portfolio-item filter-web">
          <div class="portfolio-wrap">
            <figure>
              <img src="${i5}" class="img-fluid" alt="" />
              <a
                href="${i5}"
                class="link-preview venobox"
                data-gall="portfolioGallery"
                title="Infrared_color"
                target="_blank"
                ><i class="ion ion-eye"></i
              ></a>
            </figure>

            <div class="portfolio-info">
              <h4><a href="portfolio-details.html">Infrared_color</a></h4>
              <p>${t5}</p>
            </div>
          </div>
        </div>

        <div class="col-lg-4 col-md-6 portfolio-item filter-app">
          <div class="portfolio-wrap">
            <figure>
              <img src="${i6}" class="img-fluid" alt="" />
              <a
                href="${i6}"
                class="link-preview venobox"
                data-gall="portfolioGallery"
                title="Moisture index"
                target="_blank"
                ><i class="ion ion-eye"></i
              ></a>
            </figure>

            <div class="portfolio-info">
              <h4><a href="portfolio-details.html">Moisture index</a></h4>
              <p>${t6}</p>
            </div>
          </div>
        </div>

        <div class="col-lg-4 col-md-6 portfolio-item filter-app">
          <div class="portfolio-wrap">
            <figure>
              <img src="${i7}" class="img-fluid" alt="" />
              <a
                href="${i7}"
                class="link-preview venobox"
                data-gall="portfolioGallery"
                title="NDWI"
                target="_blank"
                ><i class="ion ion-eye"></i
              ></a>
            </figure>

            <div class="portfolio-info">
              <h4><a>NDWI</a></h4>
              <p>${t7}</p>
            </div>
          </div>
        </div>
        `) ); 
        // all append ends-----------------------------------------------------------------------------------------------
        console.log("vbbsfefffffffffffffffff")
        console.log(i1);
        // -------------------------------------------------------------------------
        
      },
  
      error: function(request, status, error) {
        console.log(status)
      }
  
    });
    document.getElementById("loadingmessage1").style.display = "none";
});