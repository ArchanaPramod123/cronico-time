// $(document).ready(function(){
//     //add to cart
//     $(document).on('click',"#addToCartBtn",function(){
//         var _vm=$(this);
//         var _qty=$("#productQty").val();
//         var _productId=$(".product-id").val();
//         var _productImage=$(".product-image-one").val();
//         var _productName=$(".product-name").val();
//         var _productPrice=$(".product-price1").text();
//         var _productColor=$(".product-color1").text();

//         console.log(_qty,_productId,_productName,_productImage,_productPrice,_productColor)
//         //ajax
//         $.ajax({
//             url:'/add-to-cart',
//             data:{
//                 'id':_productId,
//                 'image':_productImage,
//                 'qty':_qty,
//                 'name':_productName,
//                 'price':_productPrice,
//                 'color':_productColor
//             },
//             dataType:'json',
//             beforeSend:function(){
//                _vm.attr('disabled',true);
//             },
//             success:function(res){
//                 // console.log(res);
//                 $(".cart-list").text(res.totalitems);
//                 _vm.attr('disabled',false);
//             }
//         });
//         //end ajax
//     });

//     //end

//     //delete item from cart
//     $(document).on('click','.delete-item',function(){
//         var _pId=$(this).attr('data-item');
//         var _vm=$(this);
//         //ajax 
//         $.ajax({
//             url:'/delete-from-cart',
//             data:{
//                 'id':_pId,
//             },
//             dataType:'json',
//             beforeSend:function(){
//                _vm.attr('disabled',true);
//             },
//             success:function(res){
//                 // console.log(res);
//                 $(".cart-list").text(res.totalitems);
//                 _vm.attr('disabled',false);
//                 $("#cartList").html(res.data);
//             }
//         }); 
//         //end
//     });

//     //end

//     //update item from cart
//     $(document).on('click','.update-item',function(){
//         var _pId=$(this).attr('data-item');
//         var _pQty=$(".product-qty-"+_pId).val()
//         var _vm=$(this);
//         //ajax 
//         $.ajax({
//             url:'/update-cart',
//             data:{
//                 'id':_pId,
//                 'qty':_pQty,
//             },
//             dataType:'json',
//             beforeSend:function(){
//                _vm.attr('disabled',true);
//             },
//             success:function(res){
//                 // console.log(res);
//                 // $(".cart-list").text(res.totalitems);
//                 _vm.attr('disabled',false);
//                 $("#cartList").html(res.data);
//             }
//         }); 
//         //end
//     });

//     //end

    


// });

// $(document).ready(function() {
//     $("#size").change(function() {
//         var selectedSizeId = $(this).val();
//         var productId = "{{ data.id }}";

//         $.ajax({
//             url: "/sizevariation",  // Replace with the actual URL of your Django view
//             type: "POST",
//             data: {
//                 'id': productId,
//                 'size': selectedSizeId,
//                 csrfmiddlewaretoken: "{{ csrf_token }}"
//             },
//             success: function(data) {
//                 if (data.price) {
//                     $("#price").text("Rs." + data.price);

//                 }
                
//                 // Handle the response if needed
//             },
//             error: function(error) {
//                 console.error("Error:", error);
//             }
//         });
//     });
// });