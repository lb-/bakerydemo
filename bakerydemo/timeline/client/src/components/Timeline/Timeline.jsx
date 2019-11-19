// timeline/client/src/components/Timeline/Timeline.jsx

import React from 'react';
import PropTypes from 'prop-types';

import classNames from 'classnames';
import moment from 'moment';
import CalendarTimeline from 'react-calendar-timeline';

// styles
import 'react-calendar-timeline/lib/Timeline.css'; // must include to ensure the timeline itself is styled
import './timeline.css';

const Timeline = ({ className }) => {
  const groups = [
    { id: 1, title: 'group 1' },
    { id: 2, title: 'group 2' },
  ];

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

  return (
    <div className={classNames('timeline', className)}>
      <CalendarTimeline
        groups={groups}
        items={items}
        defaultTimeStart={moment().add(-12, 'hour')}
        defaultTimeEnd={moment().add(12, 'hour')}
      />
    </div>
  );
};

Timeline.propTypes = {
  className: PropTypes.string,
};

Timeline.defaultProps = {
  className: '',
};

export default Timeline;
