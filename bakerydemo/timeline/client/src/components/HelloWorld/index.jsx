import { PureComponent } from 'react'; // eslint-disable-line import/no-extraneous-dependencies
import { string } from 'prop-types'; // eslint-disable-line import/no-extraneous-dependencies
import Timeline from 'react-calendar-timeline';
// make sure you include the timeline stylesheet or the timeline will not be styled
import 'react-calendar-timeline/lib/Timeline.css';
import moment from 'moment';

import './style.css';

const generateColor = () => `#${
  (0x1000000 + ((Math.random()) * 0xffffff))
    .toString(16)
    .substr(1, 6)
}`;

export default class HelloWorld extends PureComponent {
  static defaultProps = {
    initialColor: '#000',
  };

  static propTypes = {
    initialColor: string,
  };

  state = {
    color: this.props.initialColor,
  };

  componentWillReceiveProps({ initialColor }) {
    if (initialColor !== this.props.initialColor) {
      this.setState({ color: initialColor });
    }
  }

  getGroups = () => [{ id: 1, title: 'group 1' }, { id: 2, title: 'group 2' }];

  getItems = () => [
    {
      id: 1,
      group: 1,
      title: 'item 1',
      start_time: moment(),
      end_time: moment().add(1, 'hour'),
    },
    {
      id: 2,
      group: 2,
      title: 'item 2',
      start_time: moment().add(-0.5, 'hour'),
      end_time: moment().add(0.5, 'hour'),
    },
    {
      id: 3,
      group: 1,
      title: 'item 3',
      start_time: moment().add(2, 'hour'),
      end_time: moment().add(3, 'hour'),
    },
  ]

  handleClick = () => {
    this.setState({
      color: generateColor(),
    });
  };

  render() {
    return (
      <div className="hello">
        <h1 style={{ color: this.state.color, padding: '20px' }}>Hello World!</h1>
        <button onClick={this.handleClick}>Change color</button>
        <Timeline
          groups={this.getGroups()}
          items={this.getItems()}
          defaultTimeStart={moment().add(-12, 'hour')}
          defaultTimeEnd={moment().add(12, 'hour')}
        />
      </div>
    );
  }
}
