import { PureComponent } from 'react'; // eslint-disable-line import/no-extraneous-dependencies
import PropTypes from 'prop-types'; // eslint-disable-line import/no-extraneous-dependencies
import classNames from 'classnames';

import Timeline, {
  DateHeader,
  SidebarHeader,
  TimelineHeaders,
} from 'react-calendar-timeline';
import 'react-calendar-timeline/lib/Timeline.css'; // must include to ensure the timeline itself is styled

import Messages from './Messages';
import transform from './transform';

// styles

import './style.css';

export default class extends PureComponent {
  static defaultProps = {
    apiUrl: '/api/v2/pages/?limit=200',
    className: '',
    initialSearchValue: null,
    searchFormId: null,
  };

  static propTypes = {
    apiUrl: PropTypes.string,
    className: PropTypes.string,
    initialSearchValue: PropTypes.string,
    searchFormId: PropTypes.string,
  };

  constructor(props) {
    super(props);

    this.state = {
      defaultTimes: {},
      error: null,
      groups: [],
      isLoading: true,
      items: [],
      searchValue: props.initialSearchValue,
    };
  }

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
    const { searchFormId } = this.props;

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
      .then(transform)
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
    const {
      defaultTimes: { start, end },
      error,
      groups,
      isLoading,
      searchValue,
    } = this.state;

    return (
      <div className={classNames('timeline', this.props.className)}>
        {isLoading || error ? (
          <Messages error={error} isLoading={isLoading} />
        ) : (
          <Timeline
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
                        <strong>Search</strong>: {searchValue}
                      </p>
                    )}
                  </div>
                )}
              </SidebarHeader>
              <DateHeader unit="primaryHeader" />
              <DateHeader />
            </TimelineHeaders>
          </Timeline>
        )}
      </div>
    );
  }
}
