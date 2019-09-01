import { PureComponent } from 'react'; // eslint-disable-line import/no-extraneous-dependencies
import { string } from 'prop-types'; // eslint-disable-line import/no-extraneous-dependencies
import classNames from 'classnames';
import ReactTimeline from 'react-calendar-timeline';
import 'react-calendar-timeline/lib/Timeline.css'; // make sure you include the timeline stylesheet or the timeline will not be styled
import moment from 'moment';

import './style.css';

const groups = [{ id: 1, title: 'group 1' }, { id: 2, title: 'group 2' }];

const items = [
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
];

class Timeline extends PureComponent {
  static defaultProps = {
    className: '',
  };

  static propTypes = {
    className: string,
  };

  render() {
    return (
      <div className={classNames('timeline', this.props.className)}>
        <ReactTimeline
          defaultTimeEnd={moment().add(12, 'hour')}
          defaultTimeStart={moment().add(-12, 'hour')}
          groups={groups}
          items={items}
        />
      </div>
    );
  }
}

export default Timeline;
