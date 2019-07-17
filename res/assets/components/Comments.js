import PropTypes from 'prop-types';
import React from 'react';
import {lang} from '@pytsite/assetman';
import httpAPI from '@pytsite/http-api';
import Widget from '@pytsite/widget2/components/widget';
import Comment from './Comment';


export default class Comments extends Widget {
    static propTypes = Object.assign({}, Widget.propTypes, {
        authenticationURL: PropTypes.string.isRequired,
        isUserAuthenticated: PropTypes.bool.isRequired,
        settings: PropTypes.shape({
            maxDepth: PropTypes.number.isRequired,
            minBodyLength: PropTypes.number.isRequired,
            maxBodyLength: PropTypes.number.isRequired,
            permissions: PropTypes.shape({
                create: PropTypes.bool.isRequired,
            }).isRequired,
            statuses: PropTypes.object.isRequired,
        }),
        threadUID: PropTypes.string.isRequired,
        title: PropTypes.string,
        urls: PropTypes.shape({
            post: PropTypes.string.isRequired,
            get: PropTypes.string.isRequired,
        })
    });

    static defaultProps = {
        className: 'pytsite-widget pytsite-comments',
        title: lang.t('comments_odm@comments'),
    };

    constructor(props) {
        super(props);

        this.state = {
            comments: [],
        };

        this.fetchComments = this.fetchComments.bind(this);
        this.onCommentPost = this.onCommentPost.bind(this);
    }

    _getCommentObject(uid, commentsArray) {
        commentsArray = commentsArray || this.state.comments;

        let foundComment;
        for (let i = 0; i < commentsArray.length; ++i) {
            if (commentsArray[i].uid === uid)
                return commentsArray[i];

            else if (commentsArray[i].children.length) {
                foundComment = this._getCommentObject(uid, commentsArray[i].children);
                if (foundComment)
                    break;
            }
        }

        return foundComment;
    }

    static isElementInViewport(em) {
        const bounding = em.getBoundingClientRect();
        return (
            bounding.top >= 0 &&
            bounding.left >= 0 &&
            bounding.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
            bounding.right <= (window.innerWidth || document.documentElement.clientWidth)
        );
    };

    fetchComments() {
        httpAPI.get(this.props.urls.get).then(r => {
            this.setState({comments: r['items']});
        });
    }

    onCommentPost(commentData) {
        let comments = [...this.state.comments]; // Make a shallow array copy
        commentData['is_new'] = true;

        if (commentData.parent_uid) {
            let parentComment = this._getCommentObject(commentData.parent_uid, comments);
            if (parentComment)
                parentComment.children.push(commentData);
            else
                throw `Comment ${commentData.parent_uid} is not found`;
        } else {
            comments.push(commentData);
        }

        this.setState({comments: comments});

        const emId = `pytsite-comment-${commentData.uid}`;
        const em = document.getElementById(emId);
        if (!Comments.isElementInViewport(em)) {
            if (em.scrollIntoView !== undefined)
                em.scrollIntoView({behavior: 'smooth'});
            else
                window.location.hash = emId;
        }
    }

    componentDidMount() {
        this.fetchComments();
    }

    render() {
        return (
            <div className={this.props.className}>
                {this.props.title && (
                    <h5 className={'widget-title'}>{this.props.title}</h5>
                )}
                <Comment authenticationURL={this.props.authenticationURL}
                         data={{uid: null, children: this.state.comments}}
                         isUserAuthenticated={this.props.isUserAuthenticated}
                         onDelete={this.fetchComments}
                         onReply={this.onCommentPost}
                         postURL={this.props.urls.post}
                         settings={this.props.settings}
                         threadUID={this.props.threadUID}
                />
            </div>
        )
    }
}
