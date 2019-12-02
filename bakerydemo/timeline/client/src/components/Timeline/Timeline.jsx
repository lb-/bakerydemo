// timeline/client/src/components/Timeline/Timeline.jsx

import React, { PureComponent } from 'react';
import PropTypes from 'prop-types';

import classNames from 'classnames';
import CalendarTimeline from 'react-calendar-timeline';

import Messages from './Messages';
import getTransformedResponse from './get-transformed-response';

// styles
import 'react-calendar-timeline/lib/Timeline.css'; // must include to ensure the timeline itself is styled
import './timeline.css';

class Timeline extends PureComponent {
  state = {
    defaultTimes: {},
    error: null,
    groups: [],
    isLoading: true,
    items: [],
  };

  componentDidMount() {
    this.fetchData();
  }

  /** set state to loading and then call the API for the items data */
  fetchData() {
    const { apiUrl } = this.props;
    this.setState({ isLoading: true });
    fetch(apiUrl)
      .then(response => response.json())
      .then(({ message, ...data }) => {
        if (message) throw new Error(message);
        return data;
      })
      .then(getTransformedResponse)
      .then(({ items, defaultTimes, groups }) =>
        this.setState({
          defaultTimes,
          error: null,
          groups,
          isLoading: false,
          items,
        }),
      )
      .catch(error => this.setState({ error, isLoading: false }));
  }

  render() {
    const { className } = this.props;
    const {
      defaultTimes: { start, end },
      error,
      groups,
      isLoading,
      items,
    } = this.state;

    return (
      <div className={classNames('timeline', className)}>
        {isLoading || error ? (
          <Messages error={error} isLoading={isLoading} />
        ) : (
          <CalendarTimeline
            defaultTimeEnd={end}
            defaultTimeStart={start}
            groups={groups}
            items={items}
            sidebarWidth={250}
            stackItems
          />
        )}
      </div>
    );
  }
}

Timeline.defaultProps = {
  apiUrl: '/api/v2/pages/?limit=100',
  className: '',
};

Timeline.propTypes = {
  apiUrl: PropTypes.string,
  className: PropTypes.string,
};

export default Timeline;
