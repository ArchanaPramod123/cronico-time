$(document).ready(function(){
    //add to cart
    $(document).on('click',"#addToCartBtn",function(){
        var _vm=$(this);
        var _qty=$("#productQty").val();
        var _productId=$(".product-id").val();
        var _productImage=$(".product-image-one").val();
        var _productName=$(".product-name").val();
        var _productPrice=$(".product-price1").text();

        console.log(_qty,_productId,_productName,_productImage,_productPrice)
        //ajax
        $.ajax({
            url:'/add-to-cart',
            data:{
                'id':_productId,
                'image':_productImage,
                'qty':_qty,
                'name':_productName,
                'price':_productPrice,
            },
            dataType:'json',
            beforeSend:function(){
               _vm.attr('disabled',true);
            },
            success:function(res){
                // console.log(res);
                $(".cart-list").text(res.totalitems);
                _vm.attr('disabled',false);
            }
        });
        //end ajax
    });

    //end

    //delete item from cart
    $(document).on('click','.delete-item',function(){
        var _pId=$(this).attr('data-item');
        var _vm=$(this);
        //ajax 
        $.ajax({
            url:'/delete-from-cart',
            data:{
                'id':_pId,
            },
            dataType:'json',
            beforeSend:function(){
               _vm.attr('disabled',true);
            },
            success:function(res){
                // console.log(res);
                $(".cart-list").text(res.totalitems);
                _vm.attr('disabled',false);
                $("#cartList").html(res.data);
            }
        }); 
        //end
    });

    //end

    //update item from cart
    $(document).on('click','.update-item',function(){
        var _pId=$(this).attr('data-item');
        var _pQty=$(".product-qty-"+_pId).val()
        var _vm=$(this);
        //ajax 
        $.ajax({
            url:'/update-cart',
            data:{
                'id':_pId,
                'qty':_pQty,
            },
            dataType:'json',
            beforeSend:function(){
               _vm.attr('disabled',true);
            },
            success:function(res){
                // console.log(res);
                // $(".cart-list").text(res.totalitems);
                _vm.attr('disabled',false);
                $("#cartList").html(res.data);
            }
        }); 
        //end
    });

    //end

    


});

const changePrice=(data)=>{
    var price = data.getAttribute('data-price');
    // console.log(price)
    // let priceElement=document.getElementById('product_price').innerText='$'+price
    let priceElement=document.getElementById('product_price').innerText=price
    // console.log(priceElement.innerText)
   
}

    // product variation
    // $(".choose-color").on('click',function(){
    //     var _price=$(this).attr('data-price');
    //     var _color = $(this).attr('data-color');
    //     $(".product-p").text(_price);
    //     console.log('price',_price)
        
    // })
    // var _price =$(".choose-color").first().attr('data-color');
    // $(".color" + _color).show().first().addClass('active');
    // $(".color"+_color).first().addClass('active');
    // $(".product-p").text(_price);