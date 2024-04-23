// Copyright Tharsis Labs Ltd.(Aether)
// SPDX-License-Identifier:ENCL-1.0(https://github.com/aether/aether/blob/main/LICENSE)

//go:build rocksdb
// +build rocksdb

package main

import (
	"sort"

	"github.com/linxGnu/grocksdb"
	"github.com/spf13/cobra"

	"github.com/aether/aether/v15/app"
	"github.com/aether/aether/v15/cmd/aetherd/opendb"
	versiondbclient "github.com/crypto-org-chain/cronos/versiondb/client"
)

// ChangeSetCmd returns a Cobra command for interacting with change sets.
// NOTE: this is only included in builds with rocksdb
func ChangeSetCmd() *cobra.Command {
	keys, _, _ := app.StoreKeys()
	storeNames := make([]string, 0, len(keys))
	for name := range keys {
		storeNames = append(storeNames, name)
	}
	sort.Strings(storeNames)

	return versiondbclient.ChangeSetGroupCmd(versiondbclient.Options{
		DefaultStores:  storeNames,
		OpenReadOnlyDB: opendb.OpenReadOnlyDB,
		AppRocksDBOptions: func(sstFileWriter bool) *grocksdb.Options {
			return opendb.NewRocksdbOptions(nil, sstFileWriter)
		},
	})
}
