$.fn.upload=function(e,t,n,r){if(typeof t!="object"){r=n;n=t}return this.each(function(){if($(this)[0].files[0]){var i=new FormData;i.append($(this).attr("name"),$(this)[0].files[0]);if(typeof t=="object"){for(var s in t){i.append(s,t[s])}}$.ajax({url:e,type:"POST",xhr:function(){myXhr=$.ajaxSettings.xhr();if(myXhr.upload&&r){myXhr.upload.addEventListener("progress",function(e){var t=~~(e.loaded/e.total*100);if(r&&typeof r=="function"){r(e,t)}else if(r){$(r).val(t)}},false)}return myXhr},data:i,dataType:"json",cache:false,contentType:false,processData:false,complete:function(e){var t;try{t=JSON.parse(e.responseText)}catch(r){t=e.responseText}if(n)n(t)}})}})}