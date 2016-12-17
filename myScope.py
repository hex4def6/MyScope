print('Start of day')
import logging

from flask import Flask, json, render_template
from flask_ask import Ask, request, session, question, statement


from lantz.drivers.examples import LantzSignalGenerator
from lantz import Q_

with LantzSignalGenerator('TCPIP::localhost::5678::SOCKET') as inst:
    inst.amplitude = Q_(1, 'volt')
    print('amplitude: {}'.format(inst.amplitude))

with LantzSignalGenerator('TCPIP::localhost::5678::SOCKET') as inst:
    inst.amplitude = Q_(1, 'volt')
    print('amplitude: {}'.format(inst.amplitude))

with LantzSignalGenerator('TCPIP::localhost::5678::SOCKET') as inst:
    inst.amplitude = Q_(1, 'volt')
    print('amplitude: {}'.format(inst.amplitude))


#inst = LantzSignalGenerator('TCPIP::localhost::5678::SOCKET')
#inst.initialize()

print('Loaded imports....')
#print('Device found... ' + inst.idn)



app = Flask(__name__)
ask = Ask(app, "/myScope")
logging.getLogger('flask_ask').setLevel(logging.DEBUG)


COMMAND_KEY = "COMMAND"



@ask.launch
def launch():
    card_title = render_template('card_title_msg')
    question_text = render_template('welcome_msg') 
    reprompt_text = render_template('welcome_reprompt_msg')
    return question(question_text).reprompt(reprompt_text).standard_card(title=card_title, text=question_text)


@ask.intent('MyCommandIsIntent', mapping={'command': 'Command'})
def my_command_is(command):
    card_title = render_template('card_title_msg')
    if command is not None:
        session.attributes[COMMAND_KEY] = command
        question_text = render_template('known_command_msg', command=command)
        reprompt_text = render_template('known_command_reprompt_msg')
    else:
        question_text = render_template('unknown_command_msg')
        reprompt_text = render_template('unknown_command_reprompt_msg')
    return question(question_text).reprompt(reprompt_text).simple_card(card_title, question_text)



@ask.intent('WhatsMyCommandIntent')
def whats_my_command():
    card_title = render_template('card_title_msg')
    command = session.attributes.get(COMMAND_KEY)
    if command is not None:
        if command is not 'identification':
            statement_text = render_template('known_command_bye_msg', command='error error not found')
        else:    
            statement_text = render_template('known_command_bye_msg', command=command)
        return statement(statement_text).simple_card(card_title, statement_text)
    else:
        question_text = render_template('unknown_command_reprompt_msg')
        return question(question_text).reprompt(question_text).simple_card(card_title, question_text)



@ask.intent("IDNIntent")
def IDNIntent():
    output_text = inst.idn
    print(inst.idn)
    return statement(output_text)


@ask.session_ended
def session_ended():
    inst.finalize()
    print('Session Ended!')
    return statement("")


if __name__ == '__main__':
    app.run(debug=True,use_reloader=False)
    print('Got here')
