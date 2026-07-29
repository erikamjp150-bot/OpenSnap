import React, { useEffect, useState } from 'react';
import { View, Text, Image, ScrollView, ActivityIndicator, Button } from 'react-native';

interface FeedItem {
  id: number;
  type: string;
  sender_id?: number;
  user_id?: number;
  media_url: string;
  media_type: string;
  caption?: string;
  created_at: string;
  expires_at: string;
  score: number;
}

interface FeedState {
  loading: boolean;
  error: string | null;
  items: FeedItem[];
}

const FeedScreen: React.FC = () => {
  const [state, setState] = useState<FeedState>({
    loading: true,
    error: null,
    items: [],
  });

  const fetchFeed = async () => {
    setState({ loading: true, error: null, items: [] });

    try {
      const response = await fetch('http://localhost:8000/feed/user/1');
      if (!response.ok) {
        throw new Error(`Feed load failed: ${response.status}`);
      }
      const json = await response.json();
      setState({ loading: false, error: null, items: json.items });
    } catch (error: unknown) {
      setState({ loading: false, error: error instanceof Error ? error.message : 'Unknown error', items: [] });
    }
  };

  useEffect(() => {
    fetchFeed();
  }, []);

  if (state.loading) {
    return (
      <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
        <ActivityIndicator size="large" />
        <Text>Loading your feed…</Text>
      </View>
    );
  }

  if (state.error) {
    return (
      <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center', padding: 16 }}>
        <Text style={{ color: 'red', marginBottom: 16 }}>Error: {state.error}</Text>
        <Button title="Retry" onPress={fetchFeed} />
      </View>
    );
  }

  return (
    <ScrollView style={{ flex: 1, padding: 16 }}>
      {state.items.length === 0 ? (
        <Text>No feed items available yet. Try again later.</Text>
      ) : (
        state.items.map((item) => (
          <View key={`${item.type}-${item.id}`} style={{ marginBottom: 20, borderRadius: 14, overflow: 'hidden', backgroundColor: '#fff', shadowColor: '#000', shadowOpacity: 0.08, shadowRadius: 10, elevation: 2 }}>
            <View style={{ padding: 16 }}>
              <Text style={{ fontWeight: '700', marginBottom: 8 }}>{item.type === 'story' ? 'Story' : item.type === 'snap' ? 'Snap' : 'Recommendation'}</Text>
              {item.caption ? <Text style={{ marginBottom: 8 }}>{item.caption}</Text> : null}
            </View>
            <Image source={{ uri: item.media_url }} style={{ width: '100%', height: 220, backgroundColor: '#eee' }} />
            <View style={{ padding: 12, backgroundColor: '#fafafa' }}>
              <Text style={{ fontSize: 12, color: '#555' }}>Score: {item.score.toFixed(2)}</Text>
              <Text style={{ fontSize: 12, color: '#555' }}>Expires: {new Date(item.expires_at).toLocaleString()}</Text>
            </View>
          </View>
        ))
      )}
    </ScrollView>
  );
};

export default FeedScreen;
