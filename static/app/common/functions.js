function addcart(id) {
    var csrf=$('input[name=csrfmiddlewaretoken]').val()
    $.ajax({
        type:'POST',
        url:'/axf/addcart/',
        data:{'goods_id':id},
        dataType:'json',
        headers:{'X-CSRFToken':csrf},
        success:function (data) {
            if(data.code=='200'){
                $('.counter'+id).text(data.c_num);
                getPrice();
            }
        },
        error:function (data) {
            alert('请求失败');
        }
    });
}

function reducecart(id) {
    var csrf=$('input[name=csrfmiddlewaretoken]').val()
    $.ajax({
        type:'POST',
        url:'/axf/reducecart/',
        data:{'goods_id':id},
        dataType:'json',
        headers:{'X-CSRFToken':csrf},
        success:function (data) {
            $('.counter'+id).text(data.c_num);
            getPrice();
            if(data.c_num==0){
                $('#cartinfo'+id).remove();
            }
        },
        error:function (data) {
            // alert('请求失败');
        }
    });
}

function changeCartStatus(id) {
    var csrf=$('input[name=csrfmiddlewaretoken]').val()
    $.ajax({
        type:'POST',
        url:'/axf/changecartstatus/',
        data:{'cart_id':id},
        dataType:'json',
        headers:{'X-CSRFToken':csrf},
        success:function (data) {
            if(data.code==200){
                if(data.is_select){
                   s='√';
                }else{
                   s='x';
                }
                $('#cart_goods_is_select_'+id).text(s);
                getPrice();
            }

        }
    });
}

function getPrice() {
    $.get('/axf/goodscount/',function (data) {
        if(data.code==200){
            $('#allprice').text('总价:'+data.count)
        }
    });
}
getPrice();