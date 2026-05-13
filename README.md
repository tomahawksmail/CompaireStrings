# CompaireStrings

A lightweight utility/library for comparing strings efficiently and accurately.

## Features

- Fast string comparison
- Case-sensitive and case-insensitive comparison
- Handles null and empty strings safely
- Simple and easy-to-use API
- Lightweight with minimal dependencies

---

## Installation

Clone the repository:

```bash
git clone https://github.com/tomahawksmail/CompaireStrings.git
```

Navigate to the project directory:

```bash
cd CompaireStrings
```

---

## Usage

### Example

```csharp
string first = "Hello";
string second = "hello";

bool isEqual = CompareStrings.AreEqual(first, second, ignoreCase: true);

Console.WriteLine(isEqual); // Output: True
```

---

## API

### `AreEqual(string first, string second, bool ignoreCase = false)`

Compares two strings and returns `true` if they are equal.

#### Parameters

| Parameter | Type | Description |
|----------|------|-------------|
| `first` | string | First string |
| `second` | string | Second string |
| `ignoreCase` | bool | Ignore letter casing during comparison |

#### Returns

`bool`

---

## Project Structure

```text
CompaireStrings/
│
├── src/                # Source files
├── tests/              # Unit tests
├── README.md
└── LICENSE
```

---

## Running Tests

Run tests using:

```bash
dotnet test
```

---

## Contributing

Contributions are welcome.

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to your branch
5. Open a Pull Request

---

## License

This project is licensed under the MIT License.

---

## Author

Created by TomahawksMail.

GitHub Repository:  
https://github.com/tomahawksmail/CompaireStrings
