var item_id;
var mode;
var returnAgentResponse;

function getMode(e) {
    var classNames = $(e.target).closest(".mic-button-logo-default").attr('class').split(/\s+/);
    for (var idx in classNames) {
        if (classNames[idx].includes("mic-button-logo-default-")) {
            return classNames[idx].replace("mic-button-logo-default-", "");
        }
    }
    return "";
}

function makeZeroOpacity(className) {
    $(className).removeClass("opacity-1").addClass("opacity-0");
}

function makeFullOpacity(className) {
    $(className).removeClass("opacity-0").addClass("opacity-1");
}

function showInteractiveLogo(mode="base") {
    makeZeroOpacity(`.mic-button-logo-default-${mode}`);
    makeFullOpacity(`.mic-button-logo-hover-${mode}`);
}

function showStaticLogo(mode="base") {
    makeFullOpacity(`.mic-button-logo-default-${mode}`);
    makeZeroOpacity(`.mic-button-logo-hover-${mode}`);
}

function sendTranscript(transcript, reset = false) {
    $.ajax({
        url: url_sendTranscriptAjax,
        type: 'POST',
        data: {
            "userInput": transcript,
            "reset": reset,
            "item_id": item_id,
            "inputExtras": returnAgentResponse,
            "csrfmiddlewaretoken": csrf_token,
        },
        success: function (data) {
            data.reply = data.reply.replace(/(?:\r\n|\r|\n)/g, '</p><p>');
            var appendHTML = `<div class="message-text float-right"><p>${data.reply}</p>`;
            if (data.extras != null && data.extras.mode == "Ingredients") {
                var searchHref = encodeURI(`${url_search}?q=${data.extras.ingredients}`);
                appendHTML += `<a class="btn-search-items" href="${searchHref}"><i class="fa fa-search" style="margin-right: 5px;"></i>Search Items</a>`;
            }
            if (data.extras != null && data.extras.mode == "Return") {
                returnAgentResponse = data.extras.item_name;
            }
            if (data.extras != null && data.extras.return_item_id) {
                window.location.href = `/order/${data.extras.return_item_id}`;
            }
            appendHTML += `</div>`;
            $(".modal-conversation-box").append(appendHTML);
        },
        cache: false,
    });
}

$(".mic-button").on('click', (btnClickEvent) => {
    var recognition = new webkitSpeechRecognition();
    recognition.lang = "en-GB";
    recognition.onresult = (e) => {
        var transcript = e.results[0][0].transcript;
        // var transcript = "I want to return Meatballs"

        if ($(btnClickEvent.target).closest(".mic-button").hasClass("base-mic-button")) {
            $(".transcript-modal-trigger-button").click();
            $(".modal-conversation-box").html("");
            $(".modal-conversation-box").append(`<div class="message-text float-left">${transcript}</div>`);
            sendTranscript(transcript, reset=true);
        }
        else {
            $(".modal-conversation-box").append(`<div class="message-text float-left">${transcript}</div>`);
            sendTranscript(transcript, reset=false);
        }

        showStaticLogo(mode);
    }
    recognition.start();
})

$(".mic-button-logo-default").on('mouseover', (e) => {
    mode = getMode(e);
    showInteractiveLogo(mode);
})

$(".mic-button-logo-default").on('mouseleave', (e) => {
    mode = getMode(e);
    showStaticLogo(mode);
})