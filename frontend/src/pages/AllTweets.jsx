import axios from "axios";
import { useEffect, useState } from "react";
import toast from "react-hot-toast";
import { TweetCard } from "../components/index";

const API_BASE = "http://127.0.0.1:8000";

export default function AllTweets() {
  const [tweets, setTweets] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    let cancelled = false;

    const promise = (async () => {
      setLoading(true);
      setError(null);
      try {
        const res = await axios.get(`${API_BASE}/tweet/all`);
        if (cancelled) return res;
        setTweets(Array.isArray(res.data) ? res.data : []);
        return res;
      } catch (err) {
        if (cancelled) return;
        const message =
          err.response?.data?.detail ||
          err.message ||
          "Could not load tweets. Please try again.";
        setError(
          typeof message === "string" ? message : JSON.stringify(message)
        );
        setTweets([]);
        throw err;
      } finally {
        if (!cancelled) setLoading(false);
      }
    })();

    toast.promise(promise, {
      loading: "Loading tweets...",
      success: "Tweets loaded 👍🏻!",
      error: (err) =>
        err.response?.data?.detail ||
        err.message ||
        "Could not load tweets. Please try again.",
    });

    return () => {
      cancelled = true;
    };
  }, []);

  if (loading) {
    return <div className="all-tweets all-tweets--loading" />;
  }

  if (error) {
    return (
      <div className="all-tweets all-tweets--error">
        <p role="alert">{error}</p>
        <button type="button" onClick={() => window.location.reload()}>
          Retry
        </button>
      </div>
    );
  }

  const list = tweets ?? [];

  return (
    <div className="all-tweets">
      {list.length === 0 ? (
        <p className="all-tweets__empty">No tweets yet.</p>
      ) : (
        list.map((tweet, idx) => (
          <TweetCard
            key={tweet.tweet_id ?? idx}
            profileName={tweet.profile?.name}
            content={tweet.content}
            created_at={tweet.created_at}
          />
        ))
      )}
    </div>
  );
}
