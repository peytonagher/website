// classes.hpp header file

#pragma once
#include<iostream>
#include<string>
#include<vector>
using std::string;
using std::vector;

// Item class represents a product that a store sells, has a name, quantity, and price per

class Item
{
private:
    string _name_ = "";
    int _quantity_ = 0;
    int _price_ = 0;

public:
    Item() = default;
    Item(string name, int quantity, int price) : _name_(name), _quantity_(quantity), _price_(price)
    {
        _name_ = name;
        _quantity_ = quantity;
        _price_ = price;
    };
    Item(const Item &item);
    string name() const
    {
        return _name_;
    }
    int quantity() const
    {
        return _quantity_;
    }
    int price() const
    {
        return _price_;
    }
    void name(string name);
    void quantity(int quantity);
    void price(int price);
};



// Store class represents a store that has an inventory of items, each of the Item class
// Has a name, location, and an inventory of items for sale

class Store
{
private:
    string _name_ = "";
    string _location_ = "";
    vector<Item> _items_;

public:
    Store(string name, string location) : _name_(name), _location_(location)
    {
        _name_ = name;
        _location_ = location;
    };
    Store(const Store &store);
    string name() const
    {
        return _name_;
    }
    string location() const
    {
        return _location_;
    }
    vector<Item> items() const
    {
        return _items_;
    }
    int item_size();
    void name(string name);
    void location(string location);
    void add_item(string name, int quantity, int price);
};



// cpp program file

#include "classes.hpp"
#include <iostream>
#include <iomanip>
#include <string>
#include <vector>
#include <sstream>
#include <utility>
#include <map>
#include <algorithm>
using std::cin;
using std::cout;
using std::endl;
using std::fixed;
using std::getline;
using std::istringstream;
using std::make_pair;
using std::map;
using std::ostringstream;
using std::pair;
using std::setprecision;
using std::sort;
using std::string;
using std::vector;

// Functions associated with the Item class

Item::Item(const Item &item)
{
    _name_ = item.name();
    _quantity_ = item.quantity();
    _price_ = item.price();
}

void Item::name(string name)
{
    _name_ = name;
}

void Item::quantity(int quantity)
{
    _quantity_ = quantity;
}

void Item::price(int price)
{
    _price_ = price;
}

// Functions associated with the Store class

Store::Store(const Store &store)
{
    _name_ = store.name();
    _location_ = store.location();
    _items_ = store.items();
}

void Store::name(string name)
{
    _name_ = name;
}

void Store::location(string location)
{
    _location_ = location;
}

void Store::add_item(string name, int quantity, int price)
{
    Item item(name, quantity, price);
    _items_.push_back(item);
}

int Store::item_size()
{
    return static_cast<int>(_items_.size());
}


// This purchase function handles the total price of a quantity of items
// where to buy them from, and prioritizes the cheapest option

void purchase(const vector<Store> &stores, Item &list_item, const vector<pair<int, int>> &listed_for_sale, int &item_total_price)
{
    vector<string> print_out_orders;
    ostringstream oss;
    for (pair<int, int> i : listed_for_sale)
    {
        if (stores[i.first].items()[i.second].quantity() >= list_item.quantity())
        {
            item_total_price += stores[i.first].items()[i.second].price() * list_item.quantity();
            oss << "Order " << list_item.quantity() << " from " << stores[i.first].name() << " in " << stores[i.first].location() << endl;

            print_out_orders.push_back(oss.str());
            oss.str("");
            break;
        }
        else
        {
            item_total_price += stores[i.first].items()[i.second].price() * stores[i.first].items()[i.second].quantity();
            list_item.quantity(list_item.quantity() - stores[i.first].items()[i.second].quantity());
            oss << "Order " << stores[i.first].items()[i.second].quantity() << " from " << stores[i.first].name() << " in " << stores[i.first].location();
            print_out_orders.push_back(oss.str());
            oss.str("");
        }
    }
    cout << "Total price: $" << fixed << setprecision(2) << (static_cast<double>(item_total_price) / 100.00) << endl;
    for (int i = 0; i < static_cast<int>(print_out_orders.size()); i++)
    {
        cout << print_out_orders[i] << endl;
    }
}


// This selling_stores helper function assists in finding the lowest price
// among a vector of purchase options

void selling_stores(const vector<Store> &stores, const Item &list_item, vector<pair<int, int>> &listed_for_sale)
{
    for (int i = 0; i < static_cast<int>(stores.size()); ++i)
    {
        for (int j = 0; j < static_cast<int>(stores[i].items().size()); ++j)
        {
            if (stores[i].items()[j].name() == list_item.name())
            {
                listed_for_sale.push_back(make_pair(i, j));
            }
        }
    }
    // below code makes sure that the lowest price is first

    sort(listed_for_sale.begin(), listed_for_sale.end(), [stores](pair<int, int> p1, pair<int, int> p2)
         { return (stores[p1.first].items()[p1.second].price() < stores[p2.first].items()[p2.second].price()); });
}


// This helper function grabs name and quantity information about an item

void get_item(Item &item)
{
    string item_name = "";
    int item_quantity = 0;
    string line = "";
    getline(cin, line);
    istringstream iss(line);
    iss >> item_quantity;
    iss.get();
    getline(iss, item_name);
    item.name(item_name);
    item.quantity(item_quantity);
}


// This function handles making a new store initialized with items for sale
// Gives the store a name, location, and items a name, quantity, and price

void new_store(vector<Store> &store)
{
    string store_name = "";
    string store_location = "";
    string item_name = "";
    int item_quantity = 0;
    double item_price = 0.0;
    getline(cin, store_name);
    getline(cin, store_location);
    Store new_store(store_name, store_location);
    string line = "";
    while (getline(cin, line))
    {
        if (line.length() == 0)
        {
            break;
        }
        istringstream iss(line);
        getline(iss, item_name, ',');
        iss >> item_quantity;
        iss.get();
        iss.get();
        iss >> item_price;
        new_store.add_item(item_name, item_quantity, static_cast<double>(item_price * 100));
    }
    store.push_back(new_store);
}


// This function handles input from the shopping list and starts the process
// of determining where to buy each item on the shopping list

void shopping_handler(const vector<Store> &stores, int num_shopping_items, Item list_item)
{
    int item_total_price = 0;
    int balance_due = 0;
    for (int i = 0; i < num_shopping_items; i++)
    {
        item_total_price = 0;
        get_item(list_item);

        cout << "Trying to order " << list_item.quantity() << " " << list_item.name() << "(s)." << endl;
        vector<pair<int, int>> listed_for_sale;
        selling_stores(stores, list_item, listed_for_sale);
        cout << listed_for_sale.size() << " store(s) sell " << list_item.name() << "." << endl;
        purchase(stores, list_item, listed_for_sale, item_total_price);
        balance_due += item_total_price;
    }
    cout << "Be sure to bring $" << (static_cast<double>(balance_due) / 100.00) << " when you leave for the stores." << endl;
}


// This function builds store inventories (represented as a map) depending on
// the number of stores and store contents from input

void item_handler(const vector<Store> &stores, map<string, int> inventory)
{
    for (Store s : stores)
    {
        for (Item i : s.items())
        {
            inventory[i.name()] += i.quantity();
        }
    }
    cout << "There are " << inventory.size() << " distinct item(s) available for purchase." << endl;
    for (pair<string, int> i : inventory)
    {
        cout << "There are " << i.second << " " << i.first << "(s)." << endl;
    }
}


// This function adds stores based on user input and constructs them as instances
// of Store with the new_store function

void store_handler(vector<Store> &stores, int num_stores)
{
    for (int i = 0; i < num_stores; i++)
    {
        new_store(stores);
        cout << stores[i].name() << " has " << stores[i].item_size() << " distinct items." << endl;
    }
}


int main()
{
    vector<Store> stores;
    cout << "Store Related Information (ordered by in-file order): " << endl;
    string line = "";
    getline(cin, line);
    int num_stores = stoi(line);
    cout << "There are " << num_stores << " store(s)." << endl;
    store_handler(stores, num_stores);
    cout << endl;
    cout << "Item Related Information (ordered alphabetically):" << endl;
    map<string, int> inventory;
    item_handler(stores, inventory);
    cout << endl;
    cout << "Shopping:" << endl;
    getline(cin, line);
    int num_shopping_items = stoi(line);
    Item list_item;
    shopping_handler(stores, num_shopping_items, list_item);
}