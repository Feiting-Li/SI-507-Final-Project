
# Description of the Data

## Data Sources

The data comes from the website called "https://www.nbatopshot.com/search?", which is considered as the marketplace of all NFTs created by "NBA Topshot".

## Linked List Data Structure

The scraper uses a custom linked list data structure to store the scraped data. Each node in the linked list represents a distinct collectible with the following attributes:

- `link`: The URL to the collectible on the NBA Topshot marketplace.
- `common`: The rarity tier of the collectible (e.g., Common, Rare).
- `name`: The name of the player or team associated with the collectible.
- `lowest_ask`: The lowest asking price for the collectible on the marketplace.
- `avg_sale`: The average sale price for the collectible.
- `hook_shot`: Indicates whether the collectible features a hook shot.

The linked list allows for efficient appending of new data as the scraper processes each page. Each node has a reference to the next node, creating a sequence that can be easily traversed or converted to a list for other operations, such as writing to a CSV file.

## Data Structure Serialization

For compatibility with other systems and ease of sharing, the linked list can be serialized to a JSON format. This allows for the data to be read and processed by programs that may not use the custom linked list implementation.

The serialization process converts the linked list into a list of dictionaries, with each dictionary representing a node's data. This list is then written to a JSON file, preserving the order and structure of the original linked list.
