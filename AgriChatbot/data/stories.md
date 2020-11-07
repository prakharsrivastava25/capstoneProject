## say goodbye
* goodbye
  - utter_goodbye

## bot challenge
* bot_challenge
  - utter_iamabot

## survey weather+deny
* greet
    - utter_greet
* affirm
    - utter_confirm
* weather_query
    - weather_form
    - form{"name": "weather_form"}
    - form{"name": null}
    - slot{"area": null}
    - slot{"dayshence": null}
    - utter_ask_did_that_help
* deny
    - utter_sorry
    - utter_ask_continue
* affirm
    - utter_confirm

## survey weather+affirm
* greet
    - utter_greet
* affirm
    - utter_confirm
* weather_query
    - weather_form
    - form{"name": "weather_form"}
    - form{"name": null}
    - slot{"area": null}
    - slot{"dayshence": null}
    - utter_ask_did_that_help
* affirm
    - utter_glad
    - utter_ask_continue
* affirm
    - utter_confirm

## survey weather+affirm
* greet
    - utter_greet
* affirm
    - utter_confirm
* weather_query
    - weather_form
    - form{"name": "weather_form"}
    - form{"name": null}
    - slot{"area": null}
    - slot{"dayshence": null}
    - utter_ask_did_that_help
* affirm
    - utter_glad
    - utter_ask_continue
* deny
    - utter_goodbye


## survey agri+deny
* greet
    - utter_greet
* affirm
    - utter_confirm
* agriculture_query
    - agri_form
    - form{"name": "agri_form"}
    - form{"name": null}
    - slot{"question": null}
    - utter_ask_did_that_help
* deny
    - utter_sorry
    - utter_ask_continue
* affirm
    - utter_confirm

## survey agri+affirm
* greet
    - utter_greet
* affirm
    - utter_confirm
* agriculture_query
    - agri_form
    - form{"name": "agri_form"}
    - form{"name": null}
    - slot{"question": null}
    - utter_ask_did_that_help
* affirm
    - utter_glad
    - utter_ask_continue
* affirm
    - utter_confirm

## survey agri+confirm+deny
* greet
    - utter_greet
* affirm
    - utter_confirm
* agriculture_query
    - agri_form
    - form{"name": "agri_form"}
    - form{"name": null}
    - slot{"question": null}
    - utter_ask_did_that_help
* affirm
    - utter_glad
    - utter_ask_continue
* deny
    - utter_goodbye

## survey agri+confirm+deny
* greet
    - utter_greet
* affirm
    - utter_confirm
* agriculture_query
    - agri_form
    - form{"name": "agri_form"}
    - form{"name": null}
    - slot{"question": null}
    - utter_ask_did_that_help
* affirm
    - utter_glad
    - utter_ask_continue
* deny
    - utter_goodbye



## no survey
* greet
    - utter_greet
* deny
    - utter_goodbye