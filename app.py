from flask import Flask, request, jsonify
from lib.utils import readb64
from get_pulse import getPulseApp

import argparse
import datetime


pulse_app = None


def get_pulse(frame):
    start_time = start = datetime.datetime.now()
    pulse_app.frame_count += 1

    pulse = pulse_app.main_loop(frame)

    end = datetime.datetime.now()
    time_taken = (end - start).total_seconds()
    pulse_app.avg_latency = ((pulse_app.avg_latency * (pulse_app.frame_count - 1) + time_taken)
                             / pulse_app.frame_count)
    throughput = 1 / time_taken if time_taken else 0
    pulse_app.avg_throughput = (pulse_app.avg_throughput * (pulse_app.frame_count - 1) +
                                throughput) / pulse_app.frame_count

    return {'bpm': None, 'text': 'gathering data...'}


app = Flask(__name__)


@app.route('/ping', methods=['GET'])
def health():
    return jsonify({'error': None})


@app.route('/invocations', methods=['POST'])
def invocations():
    data = request.get_json()
    # print(data)
    if data['frame']:
        return jsonify(get_pulse(readb64(data['frame'])))
    else:
        return jsonify({'error': 'unknown action'})


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Webcam pulse detector.')
    parser.add_argument('serve', default=None, nargs='?',
                        help='dummy arg used by sagemaker for endpoint deployment')
    parser.add_argument('--serial', default=None,
                        help='serial port destination for bpm data')
    parser.add_argument('--baud', default=None,
                        help='Baud rate for serial transmission')
    parser.add_argument('--udp', default=None,
                        help='udp address:port destination for bpm data')

    args = parser.parse_args()

    pulse_app = getPulseApp(args)

    try:
        app.run(host='0.0.0.0', port=8080, debug=True)
    finally:
        print('avg_throughput: ', pulse_app.avg_throughput)
        print('avg_latency: ', pulse_app.avg_latency)
