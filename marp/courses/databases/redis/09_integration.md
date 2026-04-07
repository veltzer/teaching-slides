# Integrating Redis with Applications

---

## Why Redis in Modern Applications

Redis enhances application architecture:

- **Performance acceleration**: Microsecond response times
- **Scalability enabler**: Offload from primary database
- **Simplifies architecture**: Many patterns in one tool
- **Reduces infrastructure costs**: Efficient resource usage
- **Enables real-time features**: Live data and interactions

![why_redis_in_modern_applications](svg/courses/databases/redis/09_integration/why_redis_in_modern_applications.svg)

---

## Popular Redis Client Libraries

![popular_redis_client_libraries](svg/courses/databases/redis/09_integration/popular_redis_client_libraries.svg)

---

## Client Selection Criteria

When choosing a Redis client:

1. **Feature completeness**:
    - Support for all Redis commands
    - Cluster support if needed

1. **Performance characteristics**:
    - Connection pooling
    - Pipelining support
    - Serialization options

1. **Error handling**:
    - Retry mechanisms
    - Exception management

1. **Maintenance status**:
    - Active development
    - Community support
    - Documentation quality

---

## Connection Management

Best practices for Redis connections:

![connection_management](svg/courses/databases/redis/09_integration/connection_management.svg)

---

## Connection Pool Example (Node.js)

```javascript
// Using ioredis with connection pool
const Redis = require('ioredis');

// Create a connection pool
const redisPool = new Redis.Cluster([
  {
    host: 'redis-node-1',
    port: 6379
  },
  {
    host: 'redis-node-2',
    port: 6379
  }
], {
  // Connection pool options
  maxConnections: 100,
  minConnections: 10,
  clusterRetryStrategy: (times) => {
    const delay = Math.min(100 + times * 10, 2000);
    return delay;
  },
  redisOptions: {
    connectTimeout: 10000,
    retryStrategy: (times) => {
      if (times > 10) return null;
      return Math.min(times * 50, 1000);
    }
  }
});

// Handle connection events
redisPool.on('connect', () => {
  console.log('Connected to Redis');
});

redisPool.on('error', (err) => {
  console.error('Redis connection error:', err);
});
```

---

## Connection Pool Example (Java)

```java
// Using Lettuce with connection pool
import io.lettuce.core.RedisClient;
import io.lettuce.core.api.StatefulRedisConnection;
import io.lettuce.core.support.ConnectionPoolSupport;
import org.apache.commons.pool2.impl.GenericObjectPool;
import org.apache.commons.pool2.impl.GenericObjectPoolConfig;

public class RedisConnectionPool {
    private final RedisClient client;
    private final GenericObjectPool<StatefulRedisConnection<String, String>> pool;

    public RedisConnectionPool(String redisUrl) {
        this.client = RedisClient.create(redisUrl);

        GenericObjectPoolConfig<StatefulRedisConnection<String, String>> config =
            new GenericObjectPoolConfig<>();
        config.setMaxTotal(100);
        config.setMaxIdle(20);
        config.setMinIdle(10);
        config.setTestOnBorrow(true);
        config.setTestOnReturn(true);
        config.setTestWhileIdle(true);

        this.pool = ConnectionPoolSupport.createGenericObjectPool(
            () -> client.connect(), config);
    }

    public StatefulRedisConnection<String, String> borrowConnection() {
        try {
            return pool.borrowObject();
        } catch (Exception e) {
            throw new RuntimeException("Failed to get Redis connection", e);
        }
    }

    public void returnConnection(StatefulRedisConnection<String, String> connection) {
        pool.returnObject(connection);
    }

    public void shutdown() {
        pool.close();
        client.shutdown();
    }
}
```

---

## Data Serialization

Converting application data for Redis storage:

![data_serialization](svg/courses/databases/redis/09_integration/data_serialization.svg)

---

## Serialization Examples

```python
# Python examples of different serialization approaches

import json
import pickle
import msgpack
import redis

r = redis.Redis(host='localhost', port=6379, db=0)

# Simple string value
r.set('user:name', 'John Smith')

# JSON serialization
user_data = {'id': 123, 'name': 'John Smith', 'email': 'john@example.com'}
r.set('user:123:json', json.dumps(user_data))
loaded_user = json.loads(r.get('user:123:json'))

# Python pickle serialization (binary, Python-specific)
r.set('user:123:pickle', pickle.dumps(user_data))
loaded_user_pickle = pickle.loads(r.get('user:123:pickle'))

# MessagePack serialization (compact binary)
r.set('user:123:msgpack', msgpack.packb(user_data))
loaded_user_msgpack = msgpack.unpackb(r.get('user:123:msgpack'))

# Hash storage (native Redis structure)
r.hset('user:123', mapping={
    'id': 123,
    'name': 'John Smith',
    'email': 'john@example.com'
})
user_hash = r.hgetall('user:123')
```

---

## Integrating Redis as a Cache

![integrating_redis_as_a_cache](svg/courses/databases/redis/09_integration/integrating_redis_as_a_cache.svg)

Common cache patterns:
- Cache-aside (shown above)
- Read-through
- Write-through
- Write-behind

---

## Cache Implementation Example (Node.js)

```javascript
// Node.js cache example with Express
const express = require('express');
const Redis = require('ioredis');
const app = express();

// Create Redis client
const redis = new Redis({
  host: 'localhost',
  port: 6379
});

// Cache middleware
const cacheMiddleware = (req, res, next) => {
  const key = `cache:${req.originalUrl}`;

  redis.get(key).then(cachedData => {
    if (cachedData) {
      // Cache hit
      console.log('Cache hit for', key);
      return res.json(JSON.parse(cachedData));
    }

    // Cache miss - store original send
    const originalSend = res.send;

    res.send = function(body) {
      const response = body;

      // Store in cache for 60 seconds
      redis.set(key, response, 'EX', 60).catch(err => {
        console.error('Redis cache error:', err);
      });

      // Call original send
      originalSend.call(this, body);
    };

    next();
  }).catch(err => {
    console.error('Redis error:', err);
    next();
  });
};

// API route with caching
app.get('/api/products', cacheMiddleware, (req, res) => {
  // Expensive database query or API call happens here
  // ...

  const products = [/* product data */];
  res.json(products);
});

app.listen(3000, () => {
  console.log('Server listening on port 3000');
});
```

---

## Cache Implementation Example (Spring Boot)

```java
// Spring Boot cache configuration with Redis
@Configuration
@EnableCaching
public class RedisCacheConfig {

    @Bean
    public RedisCacheManager cacheManager(RedisConnectionFactory connectionFactory) {
        // Default cache configuration
        RedisCacheConfiguration cacheConfig = RedisCacheConfiguration
            .defaultCacheConfig()
            .entryTtl(Duration.ofMinutes(10))
            .serializeValuesWith(
                RedisSerializationContext.SerializationPair.fromSerializer(
                    new GenericJackson2JsonRedisSerializer()
                )
            );

        // Different TTL for different caches
        Map<String, RedisCacheConfiguration> cacheConfigurations = new HashMap<>();
        cacheConfigurations.put("products",
            cacheConfig.entryTtl(Duration.ofMinutes(5)));
        cacheConfigurations.put("categories",
            cacheConfig.entryTtl(Duration.ofHours(1)));

        return RedisCacheManager.builder(connectionFactory)
            .cacheDefaults(cacheConfig)
            .withInitialCacheConfigurations(cacheConfigurations)
            .transactionAware()
            .build();
    }
}

// Usage in service class
@Service
public class ProductService {

    private final ProductRepository productRepository;

    @Autowired
    public ProductService(ProductRepository productRepository) {
        this.productRepository = productRepository;
    }

    @Cacheable(value = "products", key = "#id")
    public Product getProductById(Long id) {
        // Method will only be called on cache miss
        return productRepository.findById(id).orElse(null);
    }

    @CacheEvict(value = "products", key = "#product.id")
    public void updateProduct(Product product) {
        productRepository.save(product);
    }

    @CacheEvict(value = "products", allEntries = true)
    public void clearProductCache() {
        // Method will clear all entries from the "products" cache
    }
}
```

---

## Redis for Session Management

![redis_for_session_management](svg/courses/databases/redis/09_integration/redis_for_session_management.svg)

Benefits:
- Centralized session storage
- Fast access times
- Automatic expiration
- Clustered environments support

---

## Session Management Example (Express.js)

```javascript
// Express.js with connect-redis session store
const express = require('express');
const session = require('express-session');
const RedisStore = require('connect-redis').default;
const Redis = require('ioredis');

const app = express();

// Create Redis client
const redisClient = new Redis({
  host: 'localhost',
  port: 6379
});

// Configure session middleware
app.use(session({
  store: new RedisStore({ client: redisClient }),
  secret: 'your-secret-key',
  resave: false,
  saveUninitialized: false,
  cookie: {
    secure: process.env.NODE_ENV === 'production',
    httpOnly: true,
    maxAge: 24 * 60 * 60 * 1000 // 24 hours
  }
}));

// Login route
app.post('/login', (req, res) => {
  // Authenticate user (simplified)
  const user = { id: 123, username: 'example' };

  // Store user data in session
  req.session.user = user;
  req.session.authenticated = true;

  res.json({ success: true });
});

// Protected route
app.get('/profile', (req, res) => {
  if (req.session.authenticated) {
    res.json({ user: req.session.user });
  } else {
    res.status(401).json({ error: 'Unauthorized' });
  }
});

// Logout route
app.post('/logout', (req, res) => {
  req.session.destroy(err => {
    if (err) {
      return res.status(500).json({ error: 'Logout failed' });
    }
    res.json({ success: true });
  });
});

app.listen(3000, () => {
  console.log('Server listening on port 3000');
});
```

---

## Session Management Example (Spring Boot)

```java
// Spring Boot session configuration with Redis
@Configuration
@EnableRedisHttpSession(maxInactiveIntervalInSeconds = 3600)
public class SessionConfig {

    @Bean
    public LettuceConnectionFactory connectionFactory() {
        return new LettuceConnectionFactory(
            new RedisStandaloneConfiguration("localhost", 6379));
    }

    @Bean
    public RedisSerializer<Object> springSessionDefaultRedisSerializer() {
        return new GenericJackson2JsonRedisSerializer();
    }
}

// Controller using session
@RestController
public class SessionController {

    @PostMapping("/login")
    public ResponseEntity<Map<String, Object>> login(
            HttpSession session, @RequestBody LoginRequest request) {

        // Authenticate user (simplified)
        UserDetails user = new UserDetails(123L, request.getUsername());

        // Store in session
        session.setAttribute("USER", user);

        Map<String, Object> response = new HashMap<>();
        response.put("success", true);
        return ResponseEntity.ok(response);
    }

    @GetMapping("/profile")
    public ResponseEntity<?> getProfile(HttpSession session) {
        UserDetails user = (UserDetails) session.getAttribute("USER");

        if (user == null) {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).build();
        }

        return ResponseEntity.ok(user);
    }

    @PostMapping("/logout")
    public ResponseEntity<?> logout(HttpSession session) {
        session.invalidate();
        return ResponseEntity.ok().build();
    }
}
```

---

## Rate Limiting with Redis

![rate_limiting_with_redis](svg/courses/databases/redis/09_integration/rate_limiting_with_redis.svg)

---

## Rate Limiting Implementation

```javascript
// Rate limiting middleware with Express
const rateLimit = async (req, res, next) => {
  const redis = req.app.get('redis');
  const ip = req.ip;
  const endpoint = req.path;

  // Different limits for different endpoints
  const limit = endpoint.startsWith('/api/public') ? 100 : 10;
  const windowSecs = 60; // 1 minute window

  const key = `ratelimit:${ip}:${endpoint}`;

  try {
    // Increment counter
    const count = await redis.incr(key);

    // Set expiry on first request
    if (count === 1) {
      await redis.expire(key, windowSecs);
    }

    // Set headers
    res.setHeader('X-RateLimit-Limit', limit);
    res.setHeader('X-RateLimit-Remaining', Math.max(0, limit - count));

    // Check if over limit
    if (count > limit) {
      return res.status(429).json({
        error: 'Too Many Requests',
        message: `Rate limit of ${limit} requests per ${windowSecs} seconds exceeded`
      });
    }

    next();
  } catch (err) {
    console.error('Rate limiting error:', err);
    next(); // Continue on error
  }
};

// Apply to routes
app.use('/api', rateLimit);
```

---

## Redis for Job Queues

![redis_for_job_queues](svg/courses/databases/redis/09_integration/redis_for_job_queues.svg)

Benefits:
- Simple implementation
- Reliable message delivery
- Work distribution
- Task prioritization
- Delayed execution

---

## Job Queue Implementation Example

```javascript
// Simple job queue with bull (based on Redis)
const Queue = require('bull');

// Create queues
const emailQueue = new Queue('email', 'redis://localhost:6379');
const imageQueue = new Queue('image-processing', {
  redis: {
    host: 'localhost',
    port: 6379
  },
  defaultJobOptions: {
    attempts: 3,
    backoff: {
      type: 'exponential',
      delay: 1000
    },
    removeOnComplete: true
  }
});

// Producer: Add jobs to the queue
async function sendWelcomeEmail(user) {
  await emailQueue.add({
    to: user.email,
    subject: 'Welcome!',
    template: 'welcome',
    context: {
      name: user.name
    }
  });
}

async function processImage(imageId, filters) {
  // Add with priority (lower number = higher priority)
  await imageQueue.add({
    imageId,
    filters
  }, {
    priority: 2
  });
}

// Delayed job
async function scheduleReminder(userId, date) {
  await emailQueue.add({
    to: user.email,
    subject: 'Reminder',
    template: 'reminder'
  }, {
    delay: date.getTime() - Date.now() // Milliseconds from now
  });
}

// Consumer: Process jobs
emailQueue.process(async (job) => {
  const { to, subject, template, context } = job.data;
  // Process email
  console.log(`Sending ${template} email to ${to}`);
  // ... actual email sending logic
  return { sent: true, id: 'some-id' };
});

imageQueue.process(async (job) => {
  const { imageId, filters } = job.data;
  console.log(`Processing image ${imageId}`);
  // ... image processing logic
  return { processed: true };
});

// Handle events
emailQueue.on('completed', (job, result) => {
  console.log(`Job ${job.id} completed with result:`, result);
});

emailQueue.on('failed', (job, err) => {
  console.error(`Job ${job.id} failed with error:`, err);
});
```

---

## Redis for Real-time Features

![redis_for_real_time_features](svg/courses/databases/redis/09_integration/redis_for_real_time_features.svg)

---

## Chat System with Redis PubSub

```javascript
// WebSocket chat server with Redis PubSub
const WebSocket = require('ws');
const Redis = require('ioredis');
const http = require('http');
const uuid = require('uuid');

// Create HTTP server
const server = http.createServer();
const wss = new WebSocket.Server({ server });

// Create Redis clients - separate for subscribe and publish
const subClient = new Redis();
const pubClient = new Redis();

// Store client connections
const clients = new Map();

// Subscribe to chat channels
subClient.subscribe('chat:general');

subClient.on('message', (channel, message) => {
  try {
    const data = JSON.parse(message);

    // Broadcast to all connected clients for this channel
    for (const [clientId, client] of clients.entries()) {
      if (client.readyState === WebSocket.OPEN && client.channels.includes(channel)) {
        client.send(JSON.stringify({
          type: 'message',
          channel: channel.split(':')[1],
          data
        }));
      }
    }
  } catch (err) {
    console.error('Error processing message:', err);
  }
});

// Handle WebSocket connections
wss.on('connection', (ws) => {
  const clientId = uuid.v4();
  const clientChannels = ['chat:general'];

  // Store client with subscribed channels
  clients.set(clientId, {
    ws,
    channels: clientChannels
  });

  // Handle incoming messages
  ws.on('message', (data) => {
    try {
      const message = JSON.parse(data);

      if (message.type === 'chat') {
        // Publish the message to Redis
        pubClient.publish(`chat:${message.channel || 'general'}`, JSON.stringify({
          id: uuid.v4(),
          clientId,
          username: message.username,
          text: message.text,
          timestamp: Date.now()
        }));
      } else if (message.type === 'join') {
        const channel = `chat:${message.channel}`;

        if (!clientChannels.includes(channel)) {
          clientChannels.push(channel);
          subClient.subscribe(channel);
        }
      }
    } catch (err) {
      console.error('Error handling message:', err);
    }
  });

  // Handle disconnection
  ws.on('close', () => {
    clients.delete(clientId);
  });

  // Send welcome message
  ws.send(JSON.stringify({
    type: 'system',
    message: 'Connected to chat server',
    clientId
  }));
});

server.listen(8080, () => {
  console.log('Chat server listening on port 8080');
});
```

---

## Leaderboard with Redis Sorted Sets

```javascript
// Leaderboard implementation using sorted sets
const express = require('express');
const Redis = require('ioredis');
const app = express();

app.use(express.json());

const redis = new Redis({
  host: 'localhost',
  port: 6379
});

// Add or update score
app.post('/leaderboard/scores', async (req, res) => {
  const { userId, username, score } = req.body;

  if (!userId || !username || score === undefined) {
    return res.status(400).json({ error: 'Missing required fields' });
  }

  try {
    // Add/update score (higher score is better)
    await redis.zadd('leaderboard:scores', score, userId);

    // Store user details
    await redis.hset(`user:${userId}`, {
      username,
      lastUpdated: Date.now()
    });

    // Get user's rank
    const rank = await redis.zrevrank('leaderboard:scores', userId);

    res.json({
      userId,
      score,
      rank: rank !== null ? rank + 1 : null
    });
  } catch (err) {
    console.error('Error updating score:', err);
    res.status(500).json({ error: 'Failed to update score' });
  }
});

// Get top scores
app.get('/leaderboard/scores/top/:count', async (req, res) => {
  const count = parseInt(req.params.count) || 10;

  try {
    // Get top scores with their user IDs
    const leaderboard = await redis.zrevrange('leaderboard:scores', 0, count - 1, 'WITHSCORES');

    // Transform results
    const results = [];
    for (let i = 0; i < leaderboard.length; i += 2) {
      const userId = leaderboard[i];
      const score = parseInt(leaderboard[i + 1]);

      // Get user details
      const userDetails = await redis.hgetall(`user:${userId}`);

      results.push({
        rank: i / 2 + 1,
        userId,
        username: userDetails.username,
        score
      });
    }

    res.json(results);
  } catch (err) {
    console.error('Error fetching leaderboard:', err);
    res.status(500).json({ error: 'Failed to fetch leaderboard' });
  }
});

// Get user's rank and surrounding players
app.get('/leaderboard/users/:userId', async (req, res) => {
  const { userId } = req.params;
  const range = 5; // Get 5 users above and below

  try {
    // Get user's rank
    const rank = await redis.zrevrank('leaderboard:scores', userId);

    if (rank === null) {
      return res.status(404).json({ error: 'User not found in leaderboard' });
    }

    // Get surrounding ranks
    const startRank = Math.max(0, rank - range);
    const endRank = rank + range;

    const leaderboardSlice = await redis.zrevrange('leaderboard:scores', startRank, endRank, 'WITHSCORES');

    // Get score
    const score = await redis.zscore('leaderboard:scores', userId);

    // Transform results similar to previous endpoint
    const results = [];
    for (let i = 0; i < leaderboardSlice.length; i += 2) {
      const id = leaderboardSlice[i];
      const score = parseInt(leaderboardSlice[i + 1]);

      // Get user details
      const userDetails = await redis.hgetall(`user:${id}`);

      results.push({
        rank: startRank + i / 2 + 1,
        userId: id,
        username: userDetails.username,
        score
      });
    }

    res.json({
      user: {
        userId,
        rank: rank + 1,
        score: parseInt(score)
      },
      leaderboard: results
    });
  } catch (err) {
    console.error('Error fetching user rank:', err);
    res.status(500).json({ error: 'Failed to fetch user rank' });
  }
});

app.listen(3000, () => {
  console.log('Leaderboard service running on port 3000');
});
```

---

## Caching Strategies in Microservices

![caching_strategies_in_microservices](svg/courses/databases/redis/09_integration/caching_strategies_in_microservices.svg)

Key strategies:
- Per-service caching
- Shared caching for common data
- Cache invalidation coordination
- Distributed locking for updates

---

## Redis and Database Integration

![redis_and_database_integration](svg/courses/databases/redis/09_integration/redis_and_database_integration.svg)

Integration patterns:
- Write-through cache
- Cache-aside pattern
- Read replicas with Redis
- Event sourcing with Redis Streams

---

## Error Handling and Resilience

Robust Redis integration requires:

![error_handling_and_resilience](svg/courses/databases/redis/09_integration/error_handling_and_resilience.svg)
