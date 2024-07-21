import { writeRealtimeDatabase,getUserID } from "./firebasepsych1.0.js";


$(document).ready(function() {

    function getUrlParameters() {
        const urlParams = new URLSearchParams(window.location.search);
        const params = {};
      
        for (const [key, value] of urlParams.entries()) {
          params[key] = value;
        }
      
        return params;
    }
    function createRadioButtons(exStr="") {
        for (var i = 0; i <=100; i += 5) {
            var radioDiv = $("<div/>", {class: "radiogroup"});
            var id_ = "radio" + exStr + i.toString();
            var label = $("<label/>", {for: id_, id:id_+'label', text:i.toString()});
            if (i==0 || i==100) {
                var description = $("<div/>", {
                    class:"scalelab",
                    id:"scalelab"+exStr+i.toString(),
                    text:""
                });
                label = label.append(description);
            }
            var inp = $("<input/>", {
                type:"radio", 
                class:"radiobutton", 
                id: id_, 
                name:"button", 
                value:i.toString()
            });
            radioDiv = radioDiv.append(inp);
            radioDiv = radioDiv.append(label);
            radioDiv.appendTo("#radioDiv"+exStr);
            if (exStr=="Ex") {
                $("#"+id_).attr("disabled",true);
            }
        }
    }
    function createPhraseRadioButtons() {
        for (var t = 1; t <= numPhraseTrials; t+=1) {
            var phraseDiv =  $("<div/>", {class: "pad"});
            var phrase = uncertainty_phrases[shuffledPhraseIndices[t-1]];
            phraseDiv.append($("<span/>", {id:'phrase'+t.toString(), class: "sidephrase", text:phrase}));
            for (var i = 0; i <=100; i += 5) {
                var radioDiv = $("<div/>", {class: "radiogroup radiosmall"});
                var id_ = "radio" + i.toString() + '-' + t.toString();
                var label = $("<label/>", {for: id_, id:id_+'label', text:i.toString()});
                var inp = $("<input/>", {type:"radio", class:"multiradiobutton", id: id_, name:"button"+t.toString(), value:i.toString()});
                radioDiv = radioDiv.append(inp);
                radioDiv = radioDiv.append(label);
                phraseDiv.append(radioDiv);
            }
            phraseDiv.appendTo("#phraseGroup");
        }
    }
    function updateTrial() {
        let trueNumTrials =numTrials + 1;
        $('#trialCounter').text( currentTrial + ' of ' + trueNumTrials);
    }
    function fillFields(sentence, ins0, ins100, prompt, estr="") {
        $('#uncertaintySentence'+estr).text(sentence);
        $('#0inst'+estr).text(ins0.substring(3));
        $('#100inst'+estr).text(ins100.substring(5));
        $('#uncertaintyQuery'+estr).text(prompt);
    }
    function fillUncertaintyText() {
        // update text with data from sentence_data using currentTrial
        var sentenceId = shuffledIndices[currentTrial-1];
        var sentence_text = sentences[sentenceId]["prompt_example"];
        var prompt = sentences[sentenceId]["prompt_instruction"];
        var instr0 = sentences[sentenceId]["prompt_instruction_0"];
        var instr100 = sentences[sentenceId]["prompt_instruction_100"];
        fillFields(sentence_text, instr0, instr100, prompt);
    }
    function fillExampleUncertaintyText(exNum) {
        // update text with data from sentence_data using currentTrial
        var num = exNum *100;
        var sentence_data = examples["context_0"][exNum.toString()];
        var sentence_text = sentence_data["prompt_example"];
        var prompt = sentence_data["prompt_instruction"];
        var instr0 = sentence_data["prompt_instruction_0"];
        var instr100 = sentence_data["prompt_instruction_100"];

        var selectedId = "radioEx" + num.toString();
        $("#exampleTitle").text("Example " + (exNum+1).toString() + " of 2");
        $('#'+selectedId).prop("checked", true);
        $('#'+selectedId).attr("disabled",false);
        $('#'+selectedId+'label').addClass('correct');
        $('#scalelabEx'+num.toString()).text("correct answer");
        $('#scalelabEx').addClass("correct");
        fillFields(sentence_text, instr0, instr100, prompt, "Ex");
    }
    function getRandomInt(max) {
        return Math.floor(Math.random() * max);
    }
    function nextScreen(current, next) {
        $(current).hide();
        $(next).show();
    }
    function shuffleArrInd(n) {
        let indices = [...Array(n).keys()];
        let shuffledInd = indices
            .map(value => ({ value, sort: Math.random() }))
            .sort((a, b) => a.sort - b.sort)
            .map(({ value }) => value.toString());
        return shuffledInd
    }

    const uncertainty_phrases = ["highly unlikely","unlikely","uncertain","likely", "highly likely"];
    var sentence_data = data;
    var participant_responses = {};

    // database info
    const studyId = "pilot2";

    // global trial info
    let numTrials = 30;
    let numPhraseTrials = 5;
    let currentTrial = 1;
    let exampleNum = 0;

    const debug = false;

    // save prolific info to participant_data
    var participant_data = getUrlParameters();

    // URL to redirect to when experiment is complete
    const redirectURL = 'https://app.prolific.com/submissions/complete?cc=C1422VDE';

    // randomly select a set of sentences from in data.json
    let sentenceSetKeys = Object.keys(sentence_data);
    let sentenceSetId = sentenceSetKeys[getRandomInt(numTrials)];
    participant_data["sentenceSetId"] = sentenceSetId;
    const sentences = sentence_data[sentenceSetId];

    // shuffle sentence indices
    let shuffledIndices = shuffleArrInd(numTrials);
    // shuffle sanity check phrase indices
    let shuffledPhraseIndices = shuffleArrInd(numPhraseTrials);
    

    createRadioButtons();
    createRadioButtons("Ex");
    createPhraseRadioButtons();

    // Update the contents of the instruction screen and main experiment screen
    updateTrial();
    $('#proceedConsent').prop('disabled', true);

    $("#consentbox").click(function() {
        if ($("#consentbox").is(':checked')) {
            $('#proceedConsent').prop('disabled', false);
        } else {
            $('#proceedConsent').prop('disabled', true);
        }
    });
    $("#qualitybox").click(function() {
        if ($("#qualitybox").is(':checked')) {
            $('#proceedQuality').prop('disabled', false);
        } else {
            $('#proceedQuality').prop('disabled', true);
        }
    });

    var startTime = new Date().getTime();
    var questionStartTime = new Date().getTime();

    $("#consent").show();

    //"proceed" button updates
    $("#proceedConsent").click(function() {
        nextScreen("#consent", "#qualityInstructions");
        $('#proceedQuality').prop('disabled', true); // disable proceed button
    });

    $("#proceedQuality").click(function() { 
        nextScreen("#qualityInstructions", "#instructions");
    });

    $("#proceedInstructions").click( function() {
        nextScreen("#instructions", "#exampleInstructions") 
    });

    $("#proceedExInstructions").click(function() {
        nextScreen("#exampleInstructions", "#exampleBox");
        fillExampleUncertaintyText(exampleNum);
    });

    $("#proceedExample").click(function() {
        exampleNum += 1;
        if (exampleNum==1){
            $('#scalelabEx0').text("");
            $('#radioEx0').prop("checked", false);
            $('#radioEx0').attr("disabled",true);
            $('#radioEx0label').removeClass("correct");
            fillExampleUncertaintyText(exampleNum);
        } else {
            nextScreen("#exampleBox", "#mainexperiment");
            fillUncertaintyText();
            $('#proceedMain').prop('disabled', true); // disable proceed button
            questionStartTime = new Date().getTime();
        }
    });

    $("#proceedMain").click(function() {
        // participant response and sentence ID
        var response = $('input[name="button"]:checked').val();
        var key = sentenceSetId.toString() + '-' + shuffledIndices[currentTrial-1].toString();
        
        // time taken (in ms)
        var questionEndTime = new Date().getTime();
        var questionTimeTaken = questionEndTime-questionStartTime;
        participant_responses[key] = {
            "index" : currentTrial,
            "timeTaken" : questionTimeTaken,
            "response" : response
        };
        $('input[name="button"]:checked').prop('checked',false);
        $('#proceedMain').prop('disabled', true);

        if (currentTrial < numTrials) {
            currentTrial += 1;
            updateTrial();
            fillUncertaintyText();

        } else {
            nextScreen("#mainexperiment", "#sanityCheck");
            $('#proceedSanity').prop('disabled', true);
        }
        questionStartTime = new Date().getTime();
    })

    $(".radiobutton").click(function() {
        $('#proceedMain').prop('disabled', false);
    });
    $(".multiradiobutton").click(function() {
        // check that all 5 groups are checked
        for (var t = 1; t <= numPhraseTrials; t+=1) {
            if (!$('input[name="button' + t.toString() + '"]:checked').val()) {
                return;
            }
        }
        $('#proceedSanity').prop('disabled', false);
    });

    $("#proceedSanity").click(function() {
        var questionEndTime = new Date().getTime();
        var questionTimeTaken = questionEndTime-questionStartTime;
        participant_data["sanityTimeTaken"] = questionTimeTaken;

        var endTime = new Date().getTime();
        var duration = endTime-startTime;
        participant_data["totalTimeTaken"] = duration;

        for (var t = 1; t <= numPhraseTrials; t+=1) {
            var response = $('input[name="button' + t.toString() + '"]:checked').val();
            var key = 'p-' + shuffledPhraseIndices[t-1].toString();
            participant_responses[key] = {
                "index" : t,
                "phrase" : uncertainty_phrases[shuffledPhraseIndices[t-1]],
                "response" : response
            };
        } 

        participant_data["responses"] = participant_responses;

        nextScreen("#sanityCheck","#feedback");
    })

    $("#proceedFeedback").click(function() {
        // get feedback
        if ($('#feedbackbox').val().trim().length >= 1) {
            var inp = $('#feedbackbox').val().trim();
            participant_data["feedback"] = inp;
        }

        // save data to firebase
        (async ()=>{
            try {
              const firebaseUserId = await getUserID();
              const databasePath = studyId+'/participantData/'+firebaseUserId;
              writeRealtimeDatabase( databasePath , participant_data );
            } catch(e) {
              console.log(e);
            }
        })();

        nextScreen("#feedback", "#ending");

    });

    $("#finishExperiment").click(function() {
        nextScreen("#ending", "#completed");

        if (debug) {
            console.log(participant_data);
        } else {
            window.location.replace( redirectURL );
        }
        
    });
    
    
});