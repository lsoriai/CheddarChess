var delayLoadingTimeout;
var loadingTimeout;
var APEXNET_Loading = {
    /*
    options:    {
                    selector:
                    delay:
                    timeout:                
                }
    */
    show: function(options) {
        var loadingOptions = options || {};
        var selector = loadingOptions.selector || null;
        var delay = loadingOptions.delay || 0;
        var timeout = loadingOptions.timeout || 0;
        if (selector) {
            $(selector).prop('disabled', 'true');
            var idLoad = "apexnet_loading_" + selector.substring(1, selector.length);
            var width = $(selector).outerWidth();
            var height = $(selector).outerHeight();
            $(selector).wrap("<div class='positionLoader' style='display:inline-block; position:relative; width:" + width + "px; height:" + height + "px;'></div>");
            $(selector).after("<i id=" + idLoad + " class='fa fa-circle-o-notch fa-spin aloader'></i>");
        } else {
            $("body").append('<div id="apexnet_ajaxLoading" class="apexnet_ajaxLoading-cover"><div class="apexnet_ajaxLoading"><i class="fa fa-spinner fa-spin"></i></div></div>');
            delayLoadingTimeout = setTimeout('$("#apexnet_ajaxLoading").fadeIn(200);', delay || 0);
        }
        if (timeout != 0) {
            loadingTimeout = setTimeout(function(selector) {
                APEXNET_Loading.hide(selector)
            }, timeout);
        }
    },
    hide: function(selector) {
        if (selector) {

            if ($(selector).parent('.positionLoader').length == 1) {
            $(selector).unwrap();
            $('#apexnet_loading_' + selector.substring(1, selector.length)).remove();
            $(selector).removeAttr('disabled');
            }
        } else {
            clearTimeout(delayLoadingTimeout);
            $("#apexnet_ajaxLoading").fadeOut(200);
            $("#apexnet_ajaxLoading").remove();
        }
        if (loadingTimeout) {
            clearTimeout(loadingTimeout);
            loadingTimeout = null;
        }
    }
}
var APEXNET_ajaxWrapper_Library = {
    /*
options: {
                method:
                async:
                data:
                traditional:
                onBeforeSend:
                onDone:
                onFail:
                onAlways:
                isShowLoading:
                selectorLoading:
                delayLoading:
          }
*/
    ajax: function(url, options) {
        var method = options.method || "GET";
        var async = options.async || true;
        var data = options.data || {};
        var contentType = options.contentType || 'application/x-www-form-urlencoded; charset=UTF-8';
        var traditional = options.traditional || false;
        var onBeforeSend = options.onBeforeSend || null;
        var onDone = options.onDone || null;
        var onFail = options.onFail || null;
        var onAlways = options.onAlways || null;
        var isShowLoading = options.isShowLoading || false;
        var selectorLoading = options.selectorLoading || null;
        var delayLoading = options.delayLoading || 0;
        var ajaxRequest = $.ajax({
            url: url,
            type: method,
            async: async,
            cache: false,
            data: data,
            traditional: traditional,
            contentType: contentType,
            beforeSend: function(xhr) {
                if (isShowLoading) {
                    APEXNET_Loading.show({
                        selector: selectorLoading,
                        delay: delayLoading,
                    });
                }
                if (onBeforeSend) {
                    onBeforeSend(xhr);
                }
            }
        }).done(function(responseData) {
            if (onDone) onDone(responseData);
        }).fail(function(xhr, textStatus, errorThrown) {
            if (onFail) {
                onFail(xhr, textStatus, errorThrown);
            }
        }).always(function() {
            if (onAlways) {
                onAlways();
            }
            if (isShowLoading) {
                APEXNET_Loading.hide(selectorLoading);
            }
        });
        
        return ajaxRequest;
    },
}