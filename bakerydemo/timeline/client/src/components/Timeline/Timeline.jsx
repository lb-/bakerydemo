// timeline/client/src/components/Timeline/Timeline.jsx

import React, { PureComponent } from 'react';
import PropTypes from 'prop-types';

import classNames from 'classnames';

import CalendarTimeline, {
  DateHeader,
  SidebarHeader,
  TimelineHeaders,
} from 'react-calendar-timeline';

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
    searchValue: null,
  };

  componentDidMount() {
    this.fetchData();
    this.setUpSearchForm();
  }

  /** handler for search form changing */
  onSearch({ target: { value } = {} } = {}) {
    const { searchValue } = this.state;

    if (value !== searchValue) {
      this.setState({ searchValue: value });
    }
  }

  /** set up a listener on a search field that is outside this component
   * (rendered by Django/Wagtail) */
  setUpSearchForm() {
    const { initialSearchValue, searchFormId } = this.props;
    this.setState({ searchValue: initialSearchValue });

    /** set up a listener on a search field that is outside this component
     * (rendered by Django/Wagtail) */
    const searchForm = document.getElementById(searchFormId);
    if (searchForm) {
      searchForm.addEventListener('keyup', event => this.onSearch(event));
    }
  }

  /** return filtered items based on the searchValue and that
   * value being included in either the group (eg. Location Page) or title.
   * Ensure we handle combinations of upper/lowercase in either parts of data.
   */
  getFilteredItems() {
    const { items, searchValue } = this.state;

    if (searchValue) {
      return items.filter(({ group, title }) =>
        [group, title]
          .join(' ')
          .toLowerCase()
          .includes(searchValue.toLowerCase()),
      );
    }
    return items;
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
      searchValue,
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
            items={this.getFilteredItems()}
            sidebarWidth={250}
            stackItems
          >
            <TimelineHeaders>
              <SidebarHeader>
                {({ getRootProps }) => (
                  <div {...getRootProps()}>
                    {searchValue && (
                      <p className="search">
                        <strong className="search-label">Search: </strong>
                        <span className="search-value">{searchValue}</span>
                      </p>
                    )}
                  </div>
                )}
              </SidebarHeader>
              <DateHeader unit="primaryHeader" />
              <DateHeader />
            </TimelineHeaders>
          </CalendarTimeline>
        )}
      </div>
    );
  }
}

Timeline.defaultProps = {
  apiUrl: '/api/v2/pages/?limit=100',
  className: '',
  initialSearchValue: null,
  searchFormId: null,
};

Timeline.propTypes = {
  apiUrl: PropTypes.string,
  className: PropTypes.string,
  initialSearchValue: PropTypes.string,
  searchFormId: PropTypes.string,
};

export default Timeline;
