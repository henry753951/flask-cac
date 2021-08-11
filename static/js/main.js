

function regsubmitForm() {
    // jquery 表單提交
    document.getElementById("reg_btn").disabled = true;
    $("#reg").ajaxSubmit(function(message) {
      switch(message){
        case "reg_succ":
          mess="<div class='alert alert-success' role='alert'>註冊成功</div>"
          document.getElementById("output").innerHTML = mess;     
          setTimeout("location.href = '/';",1000);
          break;
        case "pw_not_same":
          mess="<div class='alert alert-danger' role='alert'>確認密碼不一致</div>"             
          break;
        case "username_was_used":
          mess="<div class='alert alert-danger' role='alert'>使用者名稱已被使用</div>"                
          break;
        case "email_was_used":
          mess="<div class='alert alert-danger' role='alert'>E-mail已被使用</div>"            
          break;
        case "pw_not_strong":
          mess="<div class='alert alert-danger' role='alert'>密碼太簡單</div>"              
          break;
        case "pw_not_UpToStandard":
          mess="<div class='alert alert-danger' role='alert'>密碼必須包含至少1個大寫字母及1個數字且長度必須達到8個字元</div>"              
          break;
        default:
          mess="<div class='alert alert-danger' role='alert'>"+message+"</div>"              
          break;
      }
      document.getElementById("reg_btn").disabled = false;     
      document.getElementById("output").innerHTML = mess;              
    });
    return false;
  }


