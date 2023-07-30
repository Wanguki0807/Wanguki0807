
<!-- modify by Jfrost -->
<?php
    $banner_field_url ="contact_banner_url";
    if (isset($banner_settings->$banner_field_url) && $banner_url = $banner_settings->$banner_field_url){
    }else{
        $banner_url = "sample_banner.jpg";
    }
?>
<section class="banner-section d-flex justify-content-center align-items-center" style="background-image:url(<?=base_url("assets/rest_banner/").$banner_url?>)">
    <div class="d-flex justify-content-center">
        <span class="text-center j-contact-title j-banner-title text-uppercase"><h3 class="mb-0"><?=$this->lang->line("contact us")?></h3></span>
    </div>
</section>
<div class="container mx-auto contact-us pt-5">
    <div class="main-wrap p-0 pb-sm-5 mx-auto">
        <div class="tab-content pb-5 row">
            <div class="col-md-4 j-left-section" style="padding-right:10px;padding-left:10px;">
                <div class="address-bar text-center text-md-left text-white">
                    <h4 class="mb-md-5 mb-3"><?= $this->lang->line("Contact Info")?></h4>
                    <h4 class="text-success mb-md-3 mb-1"><?= $myRestDetail->rest_name ?></h4>
                    <div class="mb-md-3 mb-1 j-rest-info-wrap">
                        <i class="fa fa-map-marker"></i>
                        <div class="j-address-line ml-3">
                            <p class="mb-0"> <?= $myRestDetail->address1?> </p>
                            <p class="mb-0"> <?= $myRestDetail->address2?> </p>
                        </div>
                    </div>
                    <div class="mb-md-3 mb-1 j-rest-info-wrap">
                        <i class="fa fa-envelope"></i>
                        <p class="mb-0 ml-3"><?= $myRestDetail->rest_contact_no?> </p>
                    </div>
                    <div class="j-rest-info-wrap">
                        <i class="fa fa-phone-alt"></i>
                        <p class="mb-0 ml-3"><?= $myRestDetail->rest_email?> </p>
                    </div>
                </div>
                <div class="j-location-map mt-md-3 mt-2 mb-md-0 mb-2" id="contact-map"></div>
            </div>
            <div class="col-md-8 j-right-section" style="padding-right:10px;padding-left:10px;">
                <form id = "contact-us-form">
                    <input type="hidden" name = "rest_id" value=<?=$myRestId?>>
                    <div class="">
                        <label><?= $this->lang->line("Name")?></label>
                        <div class="row">
                            <div class="col-md-6 mt-3">
                                <div class="input-group">
                                    <input type="text" name="first_name" id = "first_name" class="form-control" placeholder="First Name" >
                                </div>
                            </div>
                            <div class="col-md-6 mt-3">
                                <div class="input-group">
                                    <input type="text" name="last_name"  id = "last_name" class="form-control" placeholder="Last Name" >
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="mt-4">
                        <label><?= $this->lang->line("Email")?></label>
                        <div class="row">
                            <div class="col-md-12">
                                <div class="input-group">
                                    <input type="email" name="email"  id = "email" class="form-control">
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="">
                        <div class="row">
                            <div class="col-md-6 mt-4">
                                <label><?= $this->lang->line("Mobile")?></label>
                                <div class="input-group">
                                    <input type="text" name="mobile" id = "mobile" class="form-control">
                                </div>
                            </div>
                            <div class="col-md-6 mt-4">
                                <label><?= $this->lang->line("Phone")?></label>
                                <div class="input-group">
                                    <input type="text" name="phone" id = "phone"  class="form-control">
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="mt-4">
                        <label><?= $this->lang->line("Message")?></label>
                        <div class="row">
                            <div class="col-md-12">
                                <div class="input-group">
                                    <textarea name="message" class="form-control" id = "message"  ></textarea>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="mt-3">This site is protected by reCAPTCHA and the Google<a href="https://policies.google.com/privacy"> Privacy Policy </a> and <a href="https://policies.google.com/terms"> Terms of Service </a> apply.</div>

                    <input class="btn btn-primary mt-5" type="submit" id="contact-us-btn" value="Contact">
                </form>
            </div>
        </div>
    </div>
    <div id="wrapper" >
        <?php if (in_array("order_management",$addon_features) && ($myRestDetail->dp_option >= 1 && $myRestDetail->dp_option <= 3 )){ ?>
            <section class="homepage-section section-homepage-opening-hours">
                <div class="container section-title">
                    <span class="title-line"></span>
                    <span class="title-content"><div><?= $this->lang->line("Opening Hours")?></div></span>
                    <span class="title-line"></span>
                </div>
                <?php
                    $time_format = $myRestDetail->time_format;
                    $date_format = $myRestDetail->date_format;

                    $openingTimes = $this->db->where("rest_id",$myRestId)->get("tbl_opening_times")->row();
                    // $weekdays = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun'];
                    $weekdays = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'];
                    $now_weekday= (date("N") + 6) % 7;
                    if (isset($openingTimes)){
                        $opening_hours = $openingTimes->opening_hours;
                        $opening_hours = json_decode($opening_hours);

                        $delivery_hours = $openingTimes->delivery_hours;
                        $delivery_hours = json_decode($delivery_hours);

                        $pickup_hours = $openingTimes->pickup_hours;
                        $pickup_hours = json_decode($pickup_hours);
                    }
                    $rest_opening_time = "";
                    $rest_pickup_time = "";
                    $rest_delivery_time = "";

                    foreach ($weekdays as $key => $day) {
                        if ($now_weekday ==  $key){
                            $is_today_class = "is_today";
                        }else{
                            $is_today_class = "";
                        }

                        if(isset($opening_hours[$key])){
                            $rest_opening_time .= "<p class='$is_today_class d-flex justify-content-between'><span>$day </span>";
                            if (!empty($opening_hours[$key])){
                                foreach ($opening_hours[$key] as $okey => $ovalue) {
                                    if ($okey > 0){
                                        $rest_opening_time .=  " | " . date($time_format, strtotime($ovalue->start))  ." - ". date($time_format, strtotime($ovalue->end)) ;
                                    }else{
                                        $rest_opening_time .= "<span>  ".date($time_format, strtotime($ovalue->start))  ." - ". date($time_format, strtotime($ovalue->end)) ;
                                    }
                                }
                                $rest_opening_time .= " </span>";
                            }else{
                                $rest_opening_time .= " <span> Closed</span>";
                            }
                            $rest_opening_time .= " </p>";
                        }

                        if(isset($delivery_hours[$key])){
                            $rest_delivery_time .= "<p class='$is_today_class d-flex justify-content-between'><span>$day </span>";
                            if (!empty($delivery_hours[$key])){
                                foreach ($delivery_hours[$key] as $dkey => $dvalue) {
                                    if ($dkey > 0){
                                        $rest_delivery_time .=  " | " . date($time_format, strtotime($dvalue->start))  ." - ". date($time_format, strtotime($dvalue->end)) ;
                                    }else{
                                        $rest_delivery_time .= "<span>  ".date($time_format, strtotime($dvalue->start))  ." - ". date($time_format, strtotime($dvalue->end)) ;
                                    }
                                }
                                $rest_delivery_time .= " </span>";
                            }else{
                                $rest_delivery_time .= " <span> Closed</span>";
                            }
                            $rest_delivery_time .= "</p>";
                        }

                        if(isset($pickup_hours[$key])){
                            $rest_pickup_time .= "<p class='$is_today_class d-flex justify-content-between'><span>$day </span>";
                            if (!empty($pickup_hours[$key])){
                                foreach ($pickup_hours[$key] as $pkey => $pvalue) {
                                    if ($pkey > 0){
                                        $rest_pickup_time .=  " | " . date($time_format, strtotime($pvalue->start))  ." - ". date($time_format, strtotime($pvalue->end)) ;
                                    }else{
                                        $rest_pickup_time .= "<span>  ".date($time_format, strtotime($pvalue->start))  ." - ". date($time_format, strtotime($pvalue->end)) ;
                                    }
                                }
                                $rest_pickup_time .= " </span>";
                            }else{
                                $rest_pickup_time .= " <span> Closed</span>";
                            }
                            $rest_pickup_time .= "</p>";
                        }
                    }
                ?>
                <div class="container section-body">
                    <div class="bg-cover">
                        <div class="row oh-row mx-0">
                            <div class="col oh-col opening-hours">
                                <div class="oh-div">
                                    <h5 class="jc-heading j-blue-color mb-3"> 
                                        <?= $this->lang->line("Opening Hours")?>
                                        <div class="jc-footer_heading_bottom_1st_line"></div>
                                        <div class="jc-footer_heading_bottom_2nd_line"></div>
                                    </h5>
                                    <div class="jc-footer_wrap">
                                        <div class='week-schedule'><?= $rest_opening_time ?></div>
                                    </div>
                                </div>
                            </div>
                            <?php if($myRestDetail->dp_option == 1 || $myRestDetail->dp_option == 3){  ?>
                                <div class="col oh-col delivery-hours">
                                    <div class="oh-div">
                                        <h5 class="jc-heading j-blue-color mb-3"> 
                                            <?= $this->lang->line("Delivery Hours")?>
                                            <div class="jc-footer_heading_bottom_1st_line"></div>
                                            <div class="jc-footer_heading_bottom_2nd_line"></div>
                                        </h5>
                                        <div class="jc-footer_wrap">
                                            <div class='week-schedule'><?= $rest_delivery_time ?></div>
                                        </div>
                                    </div>
                                </div>
                            <?php }?>
                            <?php if($myRestDetail->dp_option == 2 || $myRestDetail->dp_option == 3){  ?>
                                <div class="col oh-col pickup-hours">
                                    <div class="oh-div">
                                        <h5 class="jc-heading j-blue-color mb-3"> 
                                            <?= $this->lang->line("Pickup Hours")?>
                                            <div class="jc-footer_heading_bottom_1st_line"></div>
                                            <div class="jc-footer_heading_bottom_2nd_line"></div>
                                        </h5>
                                        <div class="jc-footer_wrap">
                                            <div class='week-schedule'><?= $rest_pickup_time ?></div>
                                        </div>
                                    </div>
                                </div>
                            <?php }?>
                        </div>
                    </div>
                </div>
            </section>
        <?php }?>
    </div>                        
</div>

<script>
    $(document).ready(function () {
        grecaptcha.ready(function() {
            grecaptcha.execute('6LcQbNsaAAAAALyY3W-KNEpem4zuRZJOoah3uVTT', {action: 'contact_us'}).then(function(token) {
                $('#contact-us-form').prepend('<input type="hidden" name="g-recaptcha-response" value="' + token + '">');
            });
        });
    });
</script>

<script>
    const lat = <?=$lat?>;
    const lng = <?=$lng?>;
    var myMap;
    var geocoder;
    function initialize() {
        geocoder = new google.maps.Geocoder();
        var address ="<?= $myRestDetail->address1?>";
        centerpoint = new google.maps.LatLng(lat,lng);
        var mapOptions = {
            zoom: 13, 
            center: centerpoint, 
            mapTypeId: google.maps.MapTypeId.ROADMAP
        };
        myMap = new google.maps.Map(
            document.getElementById('contact-map'), 
            mapOptions
        );
        geocoder.geocode( { 'address': address}, function(results, status) {
            if (status == 'OK') {
                myMap.setCenter(results[0].geometry.location);
                var marker = new google.maps.Marker({
                    map: myMap,
                    position: results[0].geometry.location
                });
                marker.setMap(myMap);
            }
             else{
             alert("Can`t convert Address");
                }
        });
        
          
       
    }

  

    
    //(function(){ initialize(); })();
    $(document).ready(function() {
        initialize();
    });
</script>
<!-- modify by Jfrost rest-->

it was maden by geocord
