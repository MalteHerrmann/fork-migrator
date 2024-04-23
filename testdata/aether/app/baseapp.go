// Copyright Tharsis Labs Ltd.(Aether)
// SPDX-License-Identifier:ENCL-1.0(https://github.com/aether/aether/blob/main/LICENSE)

package app

import (
	"errors"
	"io"
)

// Close will be called in graceful shutdown in start cmd
func (app *Aether) Close() error {
	err := app.BaseApp.Close()

	if cms, ok := app.CommitMultiStore().(io.Closer); ok {
		return errors.Join(err, cms.Close())
	}

	return err
}
